# Coleta da segunda rodada

O [manifesto](manifesto_execucoes.csv) organiza as 210 conversas na coluna `ordem`. Os textos estão em [prompts](../prompts/README.md) e os parâmetros em [configuracoes.json](configuracoes.json). Cada comando coleta uma conversa; execute um de cada vez.

## ChatGPT e Gemini

A coleta é manual, nas interfaces e configurações previstas no [protocolo](../protocolo/PROTOCOLO.md). Abra uma conversa independente para cada ID e utilize o [modelo de transcrição](templates/transcricao.md). Depois, preencha no manifesto `status`, `data_hora`, `arquivo_transcricao` e `observacoes_tecnicas`. Os caminhos são relativos a esta pasta.

O ID `V2-S1-C2-QWN-T020-R1` indica cenário S1, condição C2, Qwen a 0.2 e repetição R1. `GPT-BASE` e `GEM-BASE` identificam as configurações comerciais. A tentativa (`A01`, `A02`) não é uma nova repetição experimental.

A ordem foi embaralhada dentro de blocos de cenário e repetição com semente 20261105. As sementes do Qwen seguem `100000 × cenário + 10000 × condição + 100 × repetição + turno`, reutilizadas apenas entre temperaturas da mesma combinação. Os valores já estão no manifesto; não precisam ser calculados durante a coleta.

Os [hashes da versão aprovada](../protocolo/congelamento.json) permitem detectar alterações nos materiais, sem impedir o preenchimento dos campos operacionais. Protocolo, prompts e parâmetros permanecem os aprovados na v2.0.

