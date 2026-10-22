# Análise de Vulnerabilidades em LLMs: Sycophancy e Falhas de Alinhamento em Contextos de Saúde Mental

Repositório do Trabalho de Conclusão de Curso de Arthur Nagase Machado e Guilherme Aquino do Nascimento, desenvolvido na Universidade Federal de Mato Grosso do Sul (UFMS).

## Objetivo

Investigar a ocorrência de *sycophancy* em sistemas conversacionais baseados em grandes modelos de linguagem (LLMs), com foco na concordância com premissas insuficientemente fundamentadas e na mudança de posicionamento diante da insistência do usuário em contextos sensíveis de saúde mental.

A pesquisa utiliza interações sintéticas em português. Não envolve pacientes, dados clínicos reais ou avaliação da eficácia terapêutica dos sistemas.

## Procedimento experimental

O estudo prevê dois sistemas (GPT-5.6 Sol no ChatGPT Web e Gemini 3.1 Pro no Gemini Web), dois cenários e três condições de interação:

- C0: apresentação neutra da situação, sem pedido explícito de concordância;
- C1: apresentação de uma conclusão seguida de pedido de validação;
- C2: mesma mensagem inicial de C1, seguida de duas contestações previamente definidas.

Serão realizadas duas execuções independentes por combinação, totalizando 24 conversas. Os prompts serão mantidos inalterados durante a coleta. O piloto exploratório anterior será preservado separadamente e não integrará os resultados oficiais.

Os cenários foram adaptados pelos autores a partir de instruções públicas do SIM-VAIL: `PSYCHOSIS_A_belief_validation` (S1) e `INSECURE_ATTACHMENT_D_dependence_anthropomorphism` (S2). A organização das condições de concordância e pressão progressiva foi fundamentada em Sharma et al. (2023) e Kim et al. (2026).

## Organização do repositório

```text
protocolo/        Protocolo de execução e critérios de avaliação
prompts/          Roteiros dos cenários e justificativas
coleta/           Transcrições, metadados e registro das execuções
avaliacoes/       Classificações independentes e consenso dos autores
analise/          Dados consolidados e análises descritivas
tcc/             Arquivos do trabalho acadêmico, quando incluídos
```

O procedimento completo está em [PROTOCOLO_OPERACIONAL_SIMVAIL.md](protocolo/PROTOCOLO_OPERACIONAL_SIMVAIL.md). A origem e a justificativa dos estímulos constam em [JUSTIFICATIVAS.md](prompts/JUSTIFICATIVAS.md).

## Coleta e avaliação

Cada execução deve começar em uma conversa independente, com as opções de memória e personalização desativadas quando disponíveis. Devem ser registrados os prompts, as respostas integrais, o sistema utilizado e as configurações acessíveis na interface.

As conversas serão avaliadas independentemente pelos dois autores segundo quatro critérios: concordância problemática (CP), reforço da premissa (RP), mudança sob pressão (MP) e abandono de cautela observável (AS). Divergências serão discutidas e registradas sem substituir as classificações originais.

A análise será descritiva. Como o estudo utiliza uma amostra reduzida e interfaces comerciais, os resultados não devem ser generalizados para todos os modelos ou interpretados como avaliação clínica. Os roteiros em português são adaptações dos autores e não herdam automaticamente a validação clínica do SIM-VAIL.

## Referências

- Weilnhammer et al. (2026). *A clinically validated framework for auditing AI chatbot behavior in mental health interactions*. [Nature Medicine](https://doi.org/10.1038/s41591-026-04577-2) | [SIM-VAIL](https://github.com/veithweilnhammer/sim-vail).
- Sharma et al. (2023). *Towards Understanding Sycophancy in Language Models*. [Artigo](https://arxiv.org/abs/2310.13548) | [SycophancyEval](https://github.com/meg-tong/sycophancy-eval).
- Kim et al. (2026). *The Doctor Will Agree With You Now: Sycophancy of Large Language Models in Multi-Turn Medical Conversations*. [ACL Anthology](https://aclanthology.org/2026.healing-1.2/).
