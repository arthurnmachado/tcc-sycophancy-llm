# Coleta

O [manifesto](manifesto_execucoes.csv) lista as 24 conversas previstas: dois cenários, três condições, dois sistemas e duas repetições. Arthur será o responsável pela coleta. Antes de começar, Arthur e Guilherme devem revisar e congelar o [protocolo](../protocolo/PROTOCOLO_OPERACIONAL_SIMVAIL.md).

Os 24 arquivos em [oficial/](oficial/) seguem o registro mínimo do protocolo, com os metadados conhecidos e os prompts preenchidos. A data é 22/10/2026; os horários e as respostas serão preenchidos durante a coleta. Os arquivos preparados não representam conversas concluídas.

## Como executar

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
- [piloto_exploratorio/](piloto_exploratorio/): seis conversas de 30/09/2026, com prompts anteriores aos oficiais, fora do manifesto e da análise quantitativa oficial. Seus IDs são históricos e não devem ser associados às execuções oficiais de mesmo identificador.
- [templates/](templates/): modelo de registro a preencher durante a coleta.

Depois da coleta, seguir as [instruções de avaliação](../avaliacoes/README.md).
