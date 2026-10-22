# Coleta

O [manifesto](manifesto_execucoes.csv) lista as 24 conversas previstas: dois cenários, três condições, dois sistemas e duas repetições. Antes de começar, Arthur e Guilherme devem revisar e congelar o [protocolo](../protocolo/PROTOCOLO_OPERACIONAL_SIMVAIL.md).

## Como executar

1. Escolher um ID pendente e abrir uma conversa nova, inclusive para cada repetição.
2. Conferir o sistema: `GPT` corresponde a GPT-5.6 Sol no ChatGPT Web, pensamento Médio; `GEM`, a Gemini 3.1 Pro no Gemini Web. Registrar o nome e as configurações exibidos. Se houver mudança de versão ou indisponibilidade, discutir antes de prosseguir.
3. Desativar memória e personalização quando disponíveis. No ChatGPT, usar Chat Temporário e Não personalizado, conforme o protocolo. Registrar as opções disponíveis no Gemini.
4. Enviar o prompt exato de [S1](../prompts/S1.md) ou [S2](../prompts/S2.md), sem instruções adicionais, arquivos, ferramentas ou busca. Guardar a primeira resposta integral, inclusive recusas, sem editar, regenerar ou escolher outra resposta.
5. Em C0/C1, encerrar após essa resposta. Em C2, enviar T2 e T3 na mesma conversa, cada um após a resposta anterior, sem adaptar os textos.
6. Salvar uma cópia preenchida do [modelo de transcrição](templates/modelo_transcricao.md) em [oficial/](oficial/), com o ID como nome do arquivo. Registrar horário, ordem da execução e ocorrências técnicas. Alternar a ordem dos modelos entre blocos quando possível.
7. Atualizar o manifesto com coletor, status, data/hora com fuso e caminho da transcrição relativo a esta pasta, por exemplo `oficial/S1-C2-GPT-R1.md`.

Usar `pendente`, `concluida` ou `interrompida` no status. Em caso de problema técnico, preservar o registro parcial e anotar o ocorrido antes de decidir sobre nova tentativa. Uma recusa completa é uma resposta válida.

## Organização

- [oficial/](oficial/): somente transcrições da coleta oficial, revisadas para não incluir credenciais, dados de pacientes ou conversas privadas.
- [piloto_exploratorio/](piloto_exploratorio/): material do piloto, identificado como exploratório e fora do manifesto e da análise oficial.
- [templates/](templates/): modelo de registro a preencher durante a coleta.

Depois da coleta, seguir as [instruções de avaliação](../avaliacoes/README.md).
