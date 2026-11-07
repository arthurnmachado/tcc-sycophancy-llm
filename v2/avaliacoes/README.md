# Avaliações da segunda rodada

Foram preparados registros para a avaliação independente das 210 conversas por Arthur e Guilherme, segundo a [rubrica](../protocolo/RUBRICA.md). Nos arquivos [arthur.csv](arthur.csv) e [guilherme.csv](guilherme.csv), foram preenchidos os códigos de avaliação, cenários e condições. Os campos de classificação e justificativa foram deixados vazios. O [consenso.csv](consenso.csv) foi criado apenas com o cabeçalho, para preenchimento após as avaliações independentes. As avaliações individuais e o consenso ainda não foram preenchidos.

## Pacote de Guilherme

As 210 conversas foram anonimizadas para a avaliação de Guilherme, com códigos AV001–AV210 e ordem embaralhada. O pacote local `pacote_gui_v2.zip` reuniu as conversas, o índice, a rubrica e o CSV de avaliação. Os três turnos de C2 foram mantidos juntos, na sequência original. Foram incluídas apenas as conversas selecionadas no manifesto, com exclusão das tentativas interrompidas.

Os mesmos códigos foram utilizados nos CSVs dos dois autores. A correspondência com as conversas originais foi armazenada em `privado/correspondencia.csv`, sob guarda de Arthur e fora do pacote destinado a Guilherme. A pasta do pacote, o ZIP e a pasta privada foram excluídos do versionamento pelo Git.

Foram removidos do pacote os metadados de modelo, provedor, temperatura, repetição, horário e IDs originais. Os textos das mensagens e respostas foram preservados integralmente, inclusive as autorreferências. As duas ocorrências de checklist não copiado foram acompanhadas de uma nota neutra sobre a ausência do componente. Os detalhes de falhas técnicas externos ao diálogo foram mantidos nos registros originais.

As instruções do pacote orientaram o preenchimento independente do CSV na ordem do índice, sem consulta às transcrições identificadas ou à avaliação do outro autor. Também indicaram o registro de eventual identificação inferida ou exposição anterior à origem e a manutenção de campos pendentes, com justificativa, quando o conteúdo disponível fosse insuficiente para classificar um critério.

## Registros independentes

Arthur realizou a coleta e, por esse motivo, teve acesso à origem das conversas. Para a avaliação de Guilherme, foram preparadas cópias com códigos neutros, sem metadados de modelo ou temperatura e em ordem embaralhada. O campo `id_avaliacao` identificou as mesmas conversas nos dois formulários. A correspondência entre esse código e o ID do manifesto foi armazenada separadamente, com acesso reservado a Arthur durante a avaliação independente.

A preservação dos textos integrais manteve a possibilidade de inferir o modelo por autorreferências. Por isso, foi incluído no formulário um campo para registrar identificação inferida ou exposição anterior à origem.

Cada linha do formulário incluiu campos para CP, RP, MP e AS, justificativa, evidência e anotações qualitativas da trajetória. A rubrica definiu `N/A` para MP/AS em C0/C1 e para AS sem cautela anterior observável. Para avaliações pendentes e ausência de dados, foi previsto o campo vazio. As anotações intermediárias foram destinadas à análise qualitativa, sem criação de outro critério binário.

O preenchimento do consenso foi reservado à etapa posterior às duas avaliações independentes, com preservação dos arquivos individuais. Para as divergências, foi previsto o registro dos valores originais e da decisão na justificativa, com manutenção da pendência na ausência de acordo.
