# Coleta da segunda rodada

O [manifesto](manifesto_execucoes.csv) organiza as 210 conversas na coluna `ordem`. Os textos estão em [prompts](../prompts/README.md) e os parâmetros em [configuracoes.json](configuracoes.json). Cada comando coleta uma conversa; execute um de cada vez.

## Preparar o ambiente

Na raiz do repositório:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Para informar a chave do OpenRouter sem exibi-la no terminal nem gravá-la no histórico, use Bash:

```bash
read -rs -p 'Chave OpenRouter: ' OPENROUTER_API_KEY
export OPENROUTER_API_KEY
```

A chave fica somente no ambiente local. O arquivo [.env.example](../../.env.example) mostra o nome da variável, mas não é carregado automaticamente.

## Conferir e coletar o Qwen

Há dois scripts, com funções e comentários em português:

- [conferir_materiais.py](../../scripts/conferir_materiais.py) verifica se os arquivos e o planejamento correspondem à versão aprovada.
- [coletar_qwen.py](../../scripts/coletar_qwen.py) lê uma conversa do manifesto, envia seus turnos e salva as respostas.

Primeiro, confira os materiais e visualize uma conversa sem chamar a API:

```bash
python scripts/conferir_materiais.py
python scripts/coletar_qwen.py --id V2-S1-C2-QWN-T020-R1
```

Sem `--executar`, o script apenas mostra os textos e parâmetros, sem precisar de chave ou criar registros. O ID acima é um exemplo; siga a ordem do manifesto. Para fazer a coleta real e consumir créditos:

```bash
python scripts/coletar_qwen.py --id V2-S1-C2-QWN-T020-R1 --executar
```

O script mantém o histórico e os blocos de raciocínio entre os turnos. Salva a resposta completa da API em `logs_api/ID-A01.json`, uma transcrição legível em `transcricoes/ID-A01.md` e atualiza o manifesto. Os arquivos são salvos durante a conversa para preservar uma tentativa interrompida.

Erros, respostas vazias e truncamentos encerram a tentativa, sem repetição automática. Se um reinício for autorizado, use `--nova-tentativa --executar`: ele começa desde T1, com os mesmos parâmetros e sementes, e cria `A02`, preservando `A01`. Conversas concluídas não são regeneradas; recusas completas são respostas válidas. Testes técnicos com mensagens neutras devem ser registrados separadamente, fora do manifesto experimental.

## ChatGPT e Gemini

A coleta é manual, nas interfaces e configurações previstas no [protocolo](../protocolo/PROTOCOLO.md). Abra uma conversa independente para cada ID e utilize o [modelo de transcrição](templates/transcricao.md). Depois, preencha no manifesto `status`, `data_hora`, `arquivo_transcricao` e `observacoes_tecnicas`. Os caminhos são relativos a esta pasta.

O ID `V2-S1-C2-QWN-T020-R1` indica cenário S1, condição C2, Qwen a 0.2 e repetição R1. `GPT-BASE` e `GEM-BASE` identificam as configurações comerciais. A tentativa (`A01`, `A02`) não é uma nova repetição experimental.

A ordem foi embaralhada dentro de blocos de cenário e repetição com semente 20261105. As sementes do Qwen seguem `100000 × cenário + 10000 × condição + 100 × repetição + turno`, reutilizadas apenas entre temperaturas da mesma combinação. Os valores já estão no manifesto; não precisam ser calculados durante a coleta.

Os [hashes da versão aprovada](../protocolo/congelamento.json) permitem detectar alterações nos materiais, sem impedir o preenchimento dos campos operacionais. Protocolo, prompts e parâmetros permanecem os aprovados na v2.0.

Para verificar os scripts localmente, sem acessar a API: `python -m unittest discover -s tests -v`.
