"""Verificações locais da coleta. O transporte simulado não acessa a internet."""

import csv
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
        # Limpar apenas a cópia temporária: os testes não dependem do avanço da coleta real.
        for pasta in ('logs_api', 'transcricoes'):
            for caminho in (materiais.COLETA / pasta).glob('*QWN*'):
                caminho.unlink()
        for e in self.experimentos:
            if e['modelo_codigo'] == 'QWN':
                e.update(status='pendente', data_hora='', observacoes_tecnicas='',
                         arquivo_transcricao=f"transcricoes/{e['id']}-A01.md")
        self.gravar_manifesto()
        self.experimento = next(e for e in self.experimentos if e['id'] == ID)
        self.qwen = configuracoes['sistemas']['QWN']
        self.turnos = materiais.ler_turnos('S1', 'C2')

    def gravar_manifesto(self):
        with materiais.MANIFESTO.open('w', encoding='utf-8', newline='') as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=self.experimentos[0].keys())
            escritor.writeheader()
            escritor.writerows(self.experimentos)

    def preparar_fila(self):
        # Simular só três conversas restantes para testar a fila inteira sem chamadas reais.
        for e in self.experimentos:
            if e['modelo_codigo'] == 'QWN':
                e['status'] = 'concluida'
        primeiras = sorted([e for e in self.experimentos if e['modelo_codigo'] == 'QWN'
                            and e['condicao'] == 'C0'], key=lambda e: int(e['ordem']))[:4]
        self.ja_concluida = primeiras[0]
        self.fila = primeiras[1:]
        for e in self.fila:
            e['status'] = 'pendente'
        self.gravar_manifesto()


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

    def test_simulacao_da_fila_pula_concluidas_sem_escrever(self):
        self.preparar_fila()
        antes = {p: p.read_bytes() for p in self.raiz.rglob('*') if p.is_file()}
        saida = io.StringIO()
        with patch.dict(os.environ, {}, clear=True), patch('sys.argv', ['coletar_qwen.py', '--pendentes']):
            with redirect_stdout(saida):
                self.assertEqual(coleta.main(), 0)
        self.assertNotIn(self.ja_concluida['id'], saida.getvalue())
        for e in self.fila:
            self.assertIn(e['id'], saida.getvalue())
        self.assertEqual(antes, {p: p.read_bytes() for p in self.raiz.rglob('*') if p.is_file()})


@unittest.skipIf(OpenAI is None, 'Instale requirements.txt para os testes com SDK.')
class TestesAPI(Preparacao):
    def executar(self, respostas, nova_tentativa=False, em_fila=False):
        self.pedidos = []
        def responder(requisicao):
            self.pedidos.append(json.loads(requisicao.content))
            resposta = respostas.pop(0)
            if isinstance(resposta, Exception):
                raise resposta
            return httpx.Response(200, json=resposta, headers={'x-request-id': 'teste-local'})
        with OpenAI(api_key='chave-ficticia', base_url=self.qwen['base_url'], max_retries=0,
                    http_client=httpx.Client(transport=httpx.MockTransport(responder))) as cliente:
            if em_fila:
                with patch('openai.OpenAI', return_value=cliente), patch.dict(os.environ, {'OPENROUTER_API_KEY': 'chave-ficticia'}):
                    with patch('sys.argv', ['coletar_qwen.py', '--pendentes', '--executar']), redirect_stdout(io.StringIO()):
                        return coleta.main()
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

    def test_fila_respeita_ordem_e_pula_concluidas(self):
        self.preparar_fila()
        self.assertEqual(self.executar([self.resposta() for _ in self.fila], em_fila=True), 0)
        esperados = [(int(e['seed_t1']), self.qwen['configuracoes'][e['configuracao']]['temperature']) for e in self.fila]
        self.assertEqual([(p['seed'], p['temperature']) for p in self.pedidos], esperados)
        self.assertTrue(all(len(p['messages']) == 1 for p in self.pedidos))
        registros, _ = materiais.conferir_materiais()
        self.assertTrue(all(e['status'] == 'concluida' for e in registros if e['modelo_codigo'] == 'QWN'))

    def test_fila_para_no_erro_sem_repetir_ou_pular_a_falha(self):
        self.preparar_fila()
        self.assertEqual(self.executar([self.resposta(), httpx.ReadTimeout('falha simulada')], em_fila=True), 1)
        self.assertEqual(len(self.pedidos), 2)
        registros, _ = materiais.conferir_materiais()
        status = {e['id']: e['status'] for e in registros}
        self.assertEqual([status[e['id']] for e in self.fila], ['concluida', 'interrompida', 'pendente'])
        with self.assertRaises(ValueError):
            self.executar([], em_fila=True)
        self.assertEqual(self.pedidos, [])


if __name__ == '__main__':
    unittest.main()
