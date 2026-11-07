"""Coleta uma conversa ou a fila do Qwen. Sem --executar, apenas mostra o planejamento."""

import argparse
import csv
import json
import os
import time
from datetime import datetime, timezone

from conferir_materiais import COLETA, MANIFESTO, conferir_materiais, ler_turnos


def agora():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def montar_pedido(experimento, qwen, mensagens, turno):
    """Usa os parâmetros do arquivo de configuração, sem duplicar seus valores aqui."""
    parametros = qwen['parametros_fixos']
    return {
        'model': qwen['modelo'],
        'messages': list(mensagens),
        'temperature': qwen['configuracoes'][experimento['configuracao']]['temperature'],
        'seed': int(experimento[f'seed_t{turno}']),
        'max_tokens': parametros['max_tokens'],
        'top_p': parametros['top_p'],
        'presence_penalty': parametros['presence_penalty'],
        'frequency_penalty': parametros['frequency_penalty'],
        # Estes campos são próprios do OpenRouter e entram pelo extra_body do SDK.
        'extra_body': {
            'top_k': parametros['top_k'],
            'repetition_penalty': parametros['repetition_penalty'],
            'provider': qwen['provider'],
            'reasoning': qwen['reasoning'],
        },
    }


def salvar(registro, experimento, experimentos):
    """Guarda o JSON completo, uma transcrição legível e o status no manifesto."""
    nome = f"{experimento['id']}-{registro['tentativa']}"
    log = COLETA / 'logs_api' / f'{nome}.json'
    transcricao = COLETA / 'transcricoes' / f'{nome}.md'
    log.parent.mkdir(exist_ok=True)
    transcricao.parent.mkdir(exist_ok=True)

    # Gravar primeiro em .tmp evita perder o JSON anterior se a escrita for interrompida.
    temporario = log.with_suffix('.tmp')
    temporario.write_text(json.dumps(registro, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporario.replace(log)
    texto = [f"# {nome}", '', f"Status: {registro['status']}", '']
    for numero, chamada in enumerate(registro['chamadas'], 1):
        usuario = chamada['requisicao']['messages'][-1]['content']
        texto.extend([f'## T{numero} — Usuário', '', usuario, ''])
        if chamada.get('resposta_visivel'):
            texto.extend([f'## R{numero} — Assistente', '', chamada['resposta_visivel'], ''])
    transcricao.write_text('\n'.join(texto), encoding='utf-8')

    experimento.update(status=registro['status'], data_hora=registro['inicio'],
                       arquivo_transcricao=f'transcricoes/{nome}.md',
                       observacoes_tecnicas=registro.get('erro', ''))
    temporario = MANIFESTO.with_suffix('.tmp')
    with temporario.open('w', encoding='utf-8', newline='') as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=experimentos[0].keys())
        escritor.writeheader()
        escritor.writerows(experimentos)
    temporario.replace(MANIFESTO)


def coletar(experimento, experimentos, qwen, turnos, cliente, nova_tentativa=False):
    """Envia os turnos em sequência. Qualquer falha encerra e preserva a tentativa."""
    anteriores = list((COLETA / 'logs_api').glob(f"{experimento['id']}-A*.json"))
    anteriores += list((COLETA / 'transcricoes').glob(f"{experimento['id']}-A*.md"))
    if experimento['status'] == 'concluida':
        raise ValueError('Conversa já concluída; não será regenerada.')
    for caminho in anteriores:
        if caminho.suffix == '.json' and json.loads(caminho.read_text())['status'] == 'concluida':
            raise ValueError('Já existe uma tentativa concluída; confira o manifesto.')
    if (anteriores or experimento['status'] != 'pendente') and not nova_tentativa:
        raise ValueError('Há uma tentativa anterior. Um reinício exige --nova-tentativa.')
    if nova_tentativa and not anteriores:
        raise ValueError('Não existe tentativa anterior para reiniciar.')
    numero = max((int(p.stem.rsplit('-A', 1)[1]) for p in anteriores), default=0) + 1
    registro = {
        'id_execucao': experimento['id'], 'tentativa': f'A{numero:02d}', 'versao': 'v2.0',
        'coletor': experimento['coletor'], 'ordem': experimento['ordem'],
        'prompt_sha256': experimento['prompt_sha256'], 'inicio': agora(),
        'status': 'em_andamento', 'chamadas': [],
    }
    mensagens = []  # Cada conversa, inclusive uma nova tentativa, começa sem histórico.
    salvar(registro, experimento, experimentos)
    try:
        for turno, usuario in enumerate(turnos, 1):
            mensagens.append({'role': 'user', 'content': usuario})
            chamada = {'inicio': agora(), 'requisicao': montar_pedido(experimento, qwen, mensagens, turno)}
            registro['chamadas'].append(chamada)
            salvar(registro, experimento, experimentos)  # Preserva o pedido antes de acessar a rede.
            inicio = time.monotonic()
            resposta = cliente.chat.completions.create(**chamada['requisicao'])
            chamada['latencia_segundos'] = round(time.monotonic() - inicio, 3)
            chamada['resposta_integral'] = resposta.model_dump(mode='json')
            chamada['request_id'] = getattr(resposta, '_request_id', None)

            dados = chamada['resposta_integral']
            if len(dados.get('choices', [])) != 1:
                raise ValueError('A API não retornou uma única resposta.')
            escolha = dados['choices'][0]
            assistente = escolha['message']
            conteudo = assistente.get('content') or assistente.get('refusal') or ''
            chamada['resposta_visivel'] = conteudo
            # Recusas completas são válidas. Respostas vazias ou cortadas encerram a tentativa.
            if (not conteudo.strip() or escolha['finish_reason'] != 'stop'
                    or assistente.get('tool_calls')):
                raise ValueError('Resposta vazia ou incompleta; consultar o log.')
            provedor = dados.get('provider')
            if (dados['model'] != qwen['modelo']
                    or (provedor and provedor.lower() not in ('parasail', 'parasail/fp8'))):
                raise ValueError('Modelo ou provedor divergente; consultar o log.')

            mensagem = {'role': 'assistant', 'content': conteudo}
            # O raciocínio volta exatamente como veio, conforme o exemplo do OpenRouter.
            for campo in ('reasoning_details', 'reasoning'):
                if assistente.get(campo) is not None:
                    mensagem[campo] = assistente[campo]
            mensagens.append(mensagem)
            salvar(registro, experimento, experimentos)
        registro['status'] = 'concluida'
    except (Exception, KeyboardInterrupt) as erro:
        registro['status'] = 'interrompida'
        # Erros do serviço podem conter dados sensíveis: guardar tipo e código, sem cabeçalhos ou chave.
        registro['erro'] = type(erro).__name__
        registro['http_status'] = getattr(erro, 'status_code', None)
    finally:
        registro['fim'] = agora()
        salvar(registro, experimento, experimentos)
    return registro


def main():
    argumentos = argparse.ArgumentParser(description=__doc__)
    selecao = argumentos.add_mutually_exclusive_group(required=True)
    selecao.add_argument('--id', help='ID de uma conversa no manifesto.')
    selecao.add_argument('--pendentes', action='store_true', help='Executa a fila na ordem do manifesto.')
    argumentos.add_argument('--executar', action='store_true', help='Faz chamadas reais, com consumo de créditos.')
    argumentos.add_argument('--nova-tentativa', action='store_true', help='Reinicia desde T1 e preserva a tentativa anterior.')
    opcoes = argumentos.parse_args()
    if opcoes.nova_tentativa and (opcoes.pendentes or not opcoes.executar):
        raise ValueError('--nova-tentativa exige --id e --executar.')

    # 1. Escolher uma conversa ou todas as não concluídas, na ordem já planejada.
    experimentos, configuracoes = conferir_materiais()
    if opcoes.pendentes:
        fila = sorted([e for e in experimentos if e['modelo_codigo'] == 'QWN'
                       and e['status'] != 'concluida'], key=lambda e: int(e['ordem']))
    else:
        fila = [e for e in experimentos if e['id'] == opcoes.id and e['modelo_codigo'] == 'QWN']
        if not fila:
            raise ValueError('Escolha um ID QWN do manifesto. ChatGPT e Gemini são coletados manualmente.')
    if not fila:
        print('Todas as conversas do Qwen já foram concluídas.')
        return 0
    qwen = configuracoes['sistemas']['QWN']

    # 2. Sem --executar, mostrar o plano e encerrar sem chave, rede ou novos arquivos.
    if not opcoes.executar:
        chamadas = 0
        for posicao, experimento in enumerate(fila, 1):
            turnos = ler_turnos(experimento['cenario'], experimento['condicao'])
            chamadas += len(turnos)
            print(f"[{posicao}/{len(fila)}] {experimento['id']} | {len(turnos)} turno(s) | {experimento['status']}")
            if not opcoes.pendentes:
                print(json.dumps(montar_pedido(experimento, qwen, [{'role': 'user', 'content': turnos[0]}], 1),
                                 ensure_ascii=False, indent=2))
                for numero, texto in enumerate(turnos[1:], 2):
                    print(f"T{numero} (seed {experimento[f'seed_t{numero}']}): {texto}")
        print(f'{len(fila)} conversa(s), {chamadas} chamada(s) previstas se não houver interrupções.')
        print('Somente conferência. Nenhuma chamada realizada.')
        return 0

    # 3. O SDK só é necessário para a coleta real. Desativar retries evita gerar respostas extras.
    from openai import OpenAI
    chave = os.environ.get('OPENROUTER_API_KEY')
    if not chave:
        raise ValueError('Defina OPENROUTER_API_KEY no ambiente local.')
    with OpenAI(base_url=qwen['base_url'], api_key=chave, max_retries=0, timeout=300) as cliente:
        # Uma conversa por vez. coletar() começa cada histórico vazio e salva a cada turno.
        for posicao, experimento in enumerate(fila, 1):
            print(f"[{posicao}/{len(fila)}] {experimento['id']}", flush=True)
            turnos = ler_turnos(experimento['cenario'], experimento['condicao'])
            resultado = coletar(experimento, experimentos, qwen, turnos, cliente, opcoes.nova_tentativa)
            print(f"{resultado['tentativa']}: {resultado['status']}", flush=True)
            if resultado['status'] != 'concluida':
                print('Coleta parada. Consulte o log antes de decidir sobre uma nova tentativa.')
                return 1
    print('Coleta concluída.')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, KeyError, OSError, ImportError) as erro:
        raise SystemExit(f'Coleta não realizada: {erro}')
