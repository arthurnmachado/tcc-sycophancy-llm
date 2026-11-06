# Análise descritiva

A análise da v1 considera apenas as 24 conversas oficiais do [manifesto](../coleta/manifesto_execucoes.csv), coletadas em 22/10/2026. As [avaliações independentes](../avaliacoes/README.md) e o [consenso.csv](../avaliacoes/consenso.csv) estão preenchidos. O piloto exploratório fica fora dessa análise.

## Síntese dos registros concluídos

| Critério | Ocorrências | Conversas aplicáveis | `N/A` |
|---|---:|---:|---:|
| CP | 0 | 24 | 0 |
| RP | 0 | 24 | 0 |
| MP | 0 | 8 | 16 |
| AS | 0 | 8 | 16 |

Arthur e Guilherme concordaram nas 64 classificações binárias aplicáveis (100%) e na aplicação de `N/A`. Como todos os valores binários são zero, a concordância observada não demonstra que a rubrica diferencie adequadamente todos os tipos de falha.

Os sistemas mantiveram respostas cautelosas nos estímulos e configurações avaliados. Isso não demonstra imunidade a *sycophancy*, segurança em outros contextos ou superioridade de um sistema. Esta síntese deriva dos CSVs existentes; a apresentação detalhada por execução e a discussão qualitativa podem ser desenvolvidas a partir deles.

## Critérios para apresentação da análise

Preparar uma tabela por execução com cenário, condição, modelo, repetição e CP/RP/MP/AS. Apresentar contagens e proporções por modelo, cenário e condição, identificando as duas repetições. Informar o número de casos analisados em cada comparação.

CP/RP consideram a resposta final. MP/AS se aplicam a C2; excluir `N/A` dos denominadores e informar sua frequência separadamente. Execuções incompletas e avaliações pendentes devem ser identificadas, sem receber zero por falta de registro.

Para C2, descrever a trajetória T1–T3 com trechos que sustentem mudanças de posição ou manutenção de limites. C1 e C2 são conversas independentes com a mesma mensagem inicial.

Relatar a concordância entre os avaliadores antes do consenso, por critério. Em MP/AS, considerar C2 e registrar separadamente divergências sobre a aplicação de `N/A`.

Na discussão, considerar a participação de Arthur na coleta e o conhecimento do modelo pelos dois avaliadores como possíveis fontes de viés nos julgamentos. Com duas repetições por combinação e uso de interfaces comerciais, as conclusões devem se limitar às conversas e configurações observadas, conforme o [protocolo](../protocolo/PROTOCOLO_OPERACIONAL_SIMVAIL.md).
