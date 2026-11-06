"""Confere os arquivos aprovados da v2. Não usa API nem precisa de chave."""

import csv
import hashlib
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
COLETA = RAIZ / 'v2/coleta'
MANIFESTO = COLETA / 'manifesto_execucoes.csv'

# Estes campos definem o experimento. Status, data e transcrição podem mudar na coleta.
CAMPOS_PLANEJADOS = (
    'id', 'ordem', 'cenario', 'condicao', 'modelo_codigo', 'configuracao',
    'repeticao', 'coletor', 'prompt_arquivo', 'prompt_sha256',
    'seed_t1', 'seed_t2', 'seed_t3',
)


def ler_turnos(cenario, condicao):
    """Lê as mensagens marcadas com > na seção C0, C1 ou C2 do roteiro."""
    caminho = RAIZ / 'v2/prompts' / f'{cenario}.md'
    turnos = []
    dentro_da_condicao = False
    for linha in caminho.read_text(encoding='utf-8').splitlines():
        if linha.startswith('## '):
            dentro_da_condicao = linha.startswith(f'## {condicao} —')
        if dentro_da_condicao and linha.startswith('> '):
            turnos.append(linha[2:])
    quantidade = 3 if condicao == 'C2' else 1
    if len(turnos) != quantidade:
        raise ValueError(f'{cenario}/{condicao}: quantidade de turnos incorreta.')
    return turnos


def conferir_materiais():
    """Retorna o manifesto e as configurações após conferir a versão aprovada."""
    with MANIFESTO.open(encoding='utf-8', newline='') as arquivo:
        experimentos = list(csv.DictReader(arquivo))
    configuracoes = json.loads((COLETA / 'configuracoes.json').read_text(encoding='utf-8'))
    versao = json.loads((RAIZ / 'v2/protocolo/congelamento.json').read_text(encoding='utf-8'))

    # O SHA-256 é uma assinatura do conteúdo: qualquer alteração muda o resultado.
    for nome, esperado in versao['arquivos_sha256'].items():
        atual = hashlib.sha256((RAIZ / nome).read_bytes()).hexdigest()
        if atual != esperado:
            raise ValueError(f'Arquivo diferente da versão aprovada: {nome}')

    if len(experimentos) != 210 or len({e['id'] for e in experimentos}) != 210:
        raise ValueError('O manifesto deve conter as 210 conversas, sem IDs repetidos.')

    # A assinatura do planejamento ignora os campos que serão preenchidos na coleta.
    planejamento = []
    for experimento in sorted(experimentos, key=lambda e: int(e['ordem'])):
        planejamento.append({campo: experimento[campo] for campo in CAMPOS_PLANEJADOS})
    texto = json.dumps(planejamento, sort_keys=True, ensure_ascii=False, separators=(',', ':'))
    if hashlib.sha256(texto.encode('utf-8')).hexdigest() != versao['plano_manifesto_sha256']:
        raise ValueError('O planejamento do manifesto foi alterado.')

    for numero in range(1, 8):
        cenario = f'S{numero}'
        ler_turnos(cenario, 'C0')
        if ler_turnos(cenario, 'C1')[0] != ler_turnos(cenario, 'C2')[0]:
            raise ValueError(f'{cenario}: o primeiro turno de C2 deve ser igual a C1.')
    return experimentos, configuracoes


if __name__ == '__main__':
    try:
        experimentos, _ = conferir_materiais()
        pendentes = sum(e['status'] == 'pendente' for e in experimentos)
        print(f'Materiais v2.0 conferidos: 210 conversas, 350 respostas previstas; {pendentes} pendentes.')
    except (ValueError, KeyError, OSError) as erro:
        raise SystemExit(f'Falha na conferência: {erro}')
