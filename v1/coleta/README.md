# Coleta

O [manifesto](manifesto_execucoes.csv) registra as 24 conversas da v1: dois cenários, três condições, dois sistemas e duas repetições. Arthur realizou a coleta conforme o [protocolo v1](../protocolo/PROTOCOLO_OPERACIONAL_SIMVAIL.md), que registra a revisão e o congelamento dos estímulos e da rubrica antes da rodada oficial.

As 24 conversas foram realizadas em 22/10/2026 e estão registradas em [oficial/](oficial/), com os horários, os prompts e as respostas por turno. O manifesto indica todas como concluídas.

## Procedimento utilizado na v1

As instruções abaixo documentam a rodada concluída. Novas execuções devem seguir um protocolo próprio, sem alterar ou acrescentar dados ao manifesto da v1.

1. Escolher um ID pendente e abrir uma conversa nova, inclusive para cada repetição.
2. Conferir o sistema: `GPT` corresponde a GPT-5.6 Sol no ChatGPT Web; `GEM`, a Gemini 3.1 Pro no Gemini Web. Usar nível de pensamento Médio em ambos e conferir os metadados preparados com as opções exibidas. Se houver mudança de versão ou indisponibilidade, discutir antes de prosseguir.
3. No ChatGPT, usar conversa temporária e não personalizada; no Gemini, usar conversa sem memória.
4. Enviar o prompt exato de [S1](../prompts/S1.md) ou [S2](../prompts/S2.md), sem instruções adicionais, arquivos, ferramentas ou busca. Guardar a primeira resposta integral, inclusive recusas, sem editar, regenerar ou escolher outra resposta.
5. Em C0/C1, encerrar após essa resposta. Em C2, enviar T2 e T3 na mesma conversa, cada um após a resposta anterior, sem adaptar os textos.
6. Preencher o horário e as respostas no arquivo do ID escolhido em [oficial/](oficial/), registrando eventuais ocorrências técnicas. Conferir se o prompt enviado corresponde ao preparado e preservar qualquer desvio no registro. Alternar a ordem dos modelos entre blocos quando possível.
7. Atualizar o manifesto com coletor, status, data/hora com fuso e caminho da transcrição relativo a esta pasta, por exemplo `oficial/S1-C2-GPT-R1.md`.

Usar `pendente`, `concluida` ou `interrompida` no status. Em caso de problema técnico, preservar o registro parcial e anotar o ocorrido antes de decidir sobre nova tentativa. Uma recusa completa é uma resposta válida.

## Organização

- [oficial/](oficial/): somente transcrições da coleta oficial, revisadas para não incluir credenciais, dados de pacientes ou conversas privadas.
- [Piloto exploratório](../../piloto_exploratorio/): seis conversas de 30/09/2026, com prompts anteriores aos oficiais, fora do manifesto e da análise quantitativa oficial. Seus IDs são históricos e não devem ser associados às execuções oficiais de mesmo identificador.
- [templates/](templates/): modelo de registro a preencher durante a coleta.

As [avaliações independentes e o consenso](../avaliacoes/README.md) das 24 conversas também estão concluídos.
