# Coleta da segunda rodada

O [manifesto](manifesto_execucoes.csv) registra as 210 conversas concluídas, com 350 respostas textuais, e a ordem originalmente planejada na coluna `ordem`. Os textos estão em [prompts](../prompts/README.md) e os parâmetros em [configuracoes.json](configuracoes.json). O Qwen foi coletado em sequência, uma conversa por vez. As instruções abaixo documentam a execução; conversas concluídas não serão regeneradas.

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

## Coletar a fila do Qwen

Para conferir quais conversas faltam, sem acessar a API:

```bash
python scripts/coletar_qwen.py --pendentes
```

Para coletar as restantes automaticamente, com a chave já configurada:

```bash
python scripts/coletar_qwen.py --pendentes --executar
```

A fila segue a coluna `ordem` do manifesto, pula as concluídas e executa os turnos de cada conversa com histórico próprio. Os registros são salvos durante a execução, como na coleta por ID. Mantenha o terminal aberto até o fim.

O primeiro erro encerra a fila. Ela também não pula uma conversa interrompida ao ser executada novamente: confira o log e resolva essa tentativa por ID antes de retomar a fila. Não há repetição automática nem execução simultânea de conversas.

As 126 conversas do Qwen foram concluídas, com 210 respostas. Em `S5-C0-QWN-T070-R1` e `S6-C2-QWN-T100-R1`, a tentativa A01 foi interrompida por HTTP 429 e preservada nos logs e nas transcrições. Cada conversa foi reiniciada desde T1 com os mesmos parâmetros e sementes, mediante autorização, e concluída na A02. As tentativas parciais não integram a contagem das 210 respostas selecionadas.

## ChatGPT e Gemini

A coleta manual está concluída: 42 conversas do ChatGPT e 42 do Gemini, com 140 respostas textuais registradas. Os [84 arquivos de transcrição](transcricoes/README.md) estão organizados em 42 pares para consulta. Em S1 e S2, ChatGPT e Gemini foram coletados em paralelo, na ordem dos nomes dos arquivos. Em S3–S7, a coleta do ChatGPT foi concluída primeiro e a do Gemini depois. Essa sequência difere do embaralhamento planejado; as mudanças estão documentadas, sem alterar a coluna `ordem` do manifesto.

Modelo e configuração estão preenchidos conforme informado por Arthur. A data e hora da coleta manual correspondem ao salvamento de cada arquivo, conforme confirmação do coletor, no fuso de Cuiabá (UTC−04:00). Ao atualizar o registro, capture esse horário antes de editar o cabeçalho e preserve a data de modificação do arquivo. Cole as respostas integrais e atualize no manifesto `status`, `data_hora` e `observacoes_tecnicas`. Os arquivos ainda não coletados ficam com o horário em branco. O caminho da primeira tentativa já está preenchido; os caminhos são relativos a esta pasta.

Os arquivos manuais têm espaços para respostas e só devem receber status `concluida` após o registro da conversa completa. Para uma nova tentativa autorizada, use o [modelo de transcrição](templates/transcricao.md), preserve o arquivo anterior e atualize `arquivo_transcricao` no manifesto. Os arquivos do Qwen serão criados automaticamente durante a execução do script, em Markdown e JSON, com seus horários registrados automaticamente.

O ID `V2-S1-C2-QWN-T020-R1` indica cenário S1, condição C2, Qwen a 0.2 e repetição R1. `GPT-BASE` e `GEM-BASE` identificam as configurações comerciais. A tentativa (`A01`, `A02`) não é uma nova repetição experimental.

A ordem foi embaralhada dentro de blocos de cenário e repetição com semente 20261105. As sementes do Qwen seguem `100000 × cenário + 10000 × condição + 100 × repetição + turno`, reutilizadas apenas entre temperaturas da mesma combinação. Os valores já estão no manifesto; não precisam ser calculados durante a coleta.

Os [hashes da versão aprovada](../protocolo/congelamento.json) permitem detectar alterações nos materiais, sem impedir o preenchimento dos campos operacionais. Protocolo, prompts e parâmetros permanecem os aprovados na v2.0.

Para verificar os scripts localmente, sem acessar a API: `python -m unittest discover -s tests -v`.
