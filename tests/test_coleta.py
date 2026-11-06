"""Verificações locais da coleta. O transporte simulado não acessa a internet."""

import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import conferir_materiais as materiais
import coletar_qwen as coleta

try:
    import httpx
    from openai import OpenAI
except ImportError:
    OpenAI = None

ID = 'V2-S1-C2-QWN-T020-R1'


class Preparacao(unittest.TestCase):
    def setUp(self):
        # Trabalhar em uma cópia temporária: nenhum teste preenche a coleta real.
        pasta = tempfile.TemporaryDirectory()
        self.addCleanup(pasta.cleanup)
        self.raiz = Path(pasta.name)
        shutil.copytree(materiais.RAIZ / 'v2', self.raiz / 'v2')
        for modulo, nome, valor in (
            (materiais, 'RAIZ', self.raiz),
            (materiais, 'COLETA', self.raiz / 'v2/coleta'),
            (materiais, 'MANIFESTO', self.raiz / 'v2/coleta/manifesto_execucoes.csv'),
            (coleta, 'COLETA', self.raiz / 'v2/coleta'),
            (coleta, 'MANIFESTO', self.raiz / 'v2/coleta/manifesto_execucoes.csv'),
        ):
            alteracao = patch.object(modulo, nome, valor)
            alteracao.start()
            self.addCleanup(alteracao.stop)
        self.experimentos, configuracoes = materiais.conferir_materiais()
        self.experimento = next(e for e in self.experimentos if e['id'] == ID)
        self.qwen = configuracoes['sistemas']['QWN']
        self.turnos = materiais.ler_turnos('S1', 'C2')


class TestesMateriais(Preparacao):
    def test_matriz_e_turnos(self):
        self.assertEqual(len(self.experimentos), 210)
        total = sum(len(materiais.ler_turnos(e['cenario'], e['condicao'])) for e in self.experimentos)
        self.assertEqual(total, 350)

    def test_alteracao_dos_materiais_impede_coleta(self):
        caminho = self.raiz / 'v2/prompts/S1.md'
        caminho.write_text(caminho.read_text() + '\nTexto alterado.\n')
        with self.assertRaises(ValueError):
            materiais.conferir_materiais()

    def test_alteracao_do_planejamento_impede_coleta(self):
        caminho = materiais.MANIFESTO
        caminho.write_text(caminho.read_text().replace('120101', '999999'))
        with self.assertRaises(ValueError):
            materiais.conferir_materiais()

    def test_simulacao_sem_chave_rede_ou_escrita(self):
        antes = {p: p.read_bytes() for p in self.raiz.rglob('*') if p.is_file()}
        with patch.dict(os.environ, {}, clear=True), patch('sys.argv', ['coletar_qwen.py', '--id', ID]):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(coleta.main(), 0)
        depois = {p: p.read_bytes() for p in self.raiz.rglob('*') if p.is_file()}
        self.assertEqual(antes, depois)


@unittest.skipIf(OpenAI is None, 'Instale requirements.txt para os testes com SDK.')
class TestesAPI(Preparacao):
    def executar(self, respostas, nova_tentativa=False):
        self.pedidos = []
        def responder(requisicao):
            self.pedidos.append(json.loads(requisicao.content))
            resposta = respostas.pop(0)
            if isinstance(resposta, Exception):
                raise resposta
            return httpx.Response(200, json=resposta, headers={'x-request-id': 'teste-local'})
        with OpenAI(api_key='chave-ficticia', base_url=self.qwen['base_url'], max_retries=0,
                    http_client=httpx.Client(transport=httpx.MockTransport(responder))) as cliente:
            return coleta.coletar(self.experimento, self.experimentos, self.qwen,
                                  self.turnos, cliente, nova_tentativa)

    def resposta(self, conteudo='Resposta.', termino='stop'):
        return {
            'id': 'teste', 'object': 'chat.completion', 'created': 0,
            'model': self.qwen['modelo'], 'provider': 'Parasail',
            'choices': [{'index': 0, 'finish_reason': termino, 'message': {
                'role': 'assistant', 'content': conteudo,
                'reasoning_details': [{'type': 'reasoning.encrypted', 'data': 'bloco-inalterado'}],
            }}],
        }

    def test_c2_parametros_historico_e_registros(self):
        resultado = self.executar([self.resposta() for _ in range(3)])
        self.assertEqual(resultado['status'], 'concluida')
        self.assertEqual([len(p['messages']) for p in self.pedidos], [1, 3, 5])
        self.assertEqual([p['seed'] for p in self.pedidos], [120101, 120102, 120103])
        self.assertEqual(self.pedidos[0]['provider'], self.qwen['provider'])
        for parametro, valor in self.qwen['parametros_fixos'].items():
            self.assertEqual(self.pedidos[0][parametro], valor)
        self.assertEqual(self.pedidos[1]['messages'][1]['reasoning_details'],
                         self.resposta()['choices'][0]['message']['reasoning_details'])
        self.assertEqual(resultado['chamadas'][0]['request_id'], 'teste-local')
        self.assertEqual(self.experimento['status'], 'concluida')
        materiais.conferir_materiais()  # Preencher o status não altera o planejamento.
        with self.assertRaises(ValueError):
            self.executar([self.resposta()])

    def test_timeout_sem_retry_e_reinicio_desde_t1(self):
        resultado = self.executar([self.resposta(), httpx.ReadTimeout('chave-ficticia')])
        self.assertEqual(resultado['status'], 'interrompida')
        self.assertEqual(len(self.pedidos), 2)
        arquivo = materiais.COLETA / f'logs_api/{ID}-A01.json'
        original = arquivo.read_bytes()
        self.assertNotIn('chave-ficticia', original.decode())
        with self.assertRaises(ValueError):
            self.executar([self.resposta()])
        novo = self.executar([self.resposta() for _ in range(3)], nova_tentativa=True)
        self.assertEqual(novo['tentativa'], 'A02')
        self.assertEqual(len(self.pedidos[0]['messages']), 1)
        self.assertEqual(self.pedidos[0]['seed'], 120101)
        self.assertEqual(arquivo.read_bytes(), original)

    def test_resposta_cortada_preservada_sem_enviar_proximo_turno(self):
        resultado = self.executar([self.resposta('Texto parcial.', 'length')])
        self.assertEqual(resultado['status'], 'interrompida')
        self.assertEqual(len(self.pedidos), 1)
        transcricao = materiais.COLETA / f'transcricoes/{ID}-A01.md'
        self.assertIn('Texto parcial.', transcricao.read_text())

    def test_recusa_completa_e_valida(self):
        self.experimento = next(e for e in self.experimentos if e['id'] == 'V2-S1-C0-QWN-T020-R1')
        self.turnos = materiais.ler_turnos('S1', 'C0')
        resultado = self.executar([self.resposta('Não posso apoiar essa decisão.')])
        self.assertEqual(resultado['status'], 'concluida')


if __name__ == '__main__':
    unittest.main()
