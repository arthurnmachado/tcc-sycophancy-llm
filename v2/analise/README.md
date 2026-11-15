# Análise da segunda rodada

A coleta da v2 reuniu 210 conversas e 350 respostas, registradas no [manifesto](../coleta/manifesto_execucoes.csv). As duas avaliações individuais e os registros de consenso estão em [avaliações](../avaliacoes/README.md).

O arquivo `consenso.csv` combina as classificações pela regra OR: a marcação de pelo menos um avaliador é suficiente para registrar 1. Por isso, seus resultados não devem ser interpretados como concordância entre os avaliadores. As decisões discutidas antes da aplicação do OR foram preservadas separadamente em `consenso_acordado.csv`.

As contagens devem indicar os denominadores aplicáveis e os casos `N/A`. Em C2, AS não se aplica quando não há cautela anterior observável. A comparação entre C1 e C2 exige considerar que as conversas têm durações diferentes. As temperaturas foram variadas apenas para o Qwen; as demais condições de coleta dos modelos também devem ser consideradas na comparação.

Arthur conhecia a origem das respostas por ter realizado a coleta. Guilherme recebeu cópias sem os metadados de modelo e configuração, embora o próprio texto pudesse conter autorreferências. A v1 e o piloto são conjuntos distintos e não integram os denominadores da v2.
