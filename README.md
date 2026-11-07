# Sycophancy e falhas de alinhamento em contextos de saúde mental

Repositório do Trabalho de Conclusão de Curso de Arthur Nagase Machado e Guilherme Aquino do Nascimento, do curso de Engenharia de Computação da Universidade Federal de Mato Grosso do Sul.

A pesquisa examina o comportamento de sistemas conversacionais diante de interpretações, preferências e intenções apresentadas em interações sintéticas em português. Os cenários são adaptações autorais de instruções públicas do SIM-VAIL. O estudo não envolve participantes humanos ou dados clínicos reais e não avalia eficácia terapêutica.

## Organização

```text
piloto_exploratorio/  Teste preliminar de setembro de 2026
v1/                  Primeira rodada: protocolo, estímulos, coleta e avaliações
v2/                  Segunda rodada: materiais aprovados e coleta
```

Cada rodada reúne seus próprios materiais e dados. A numeração dos cenários é temática: S1 e S2 aparecem nas duas rodadas, mas seus estímulos foram reformulados na v2. Os identificadores e resultados do piloto não integram as rodadas oficiais.

## Primeira rodada

A [v1](v1/README.md) compreende 24 conversas coletadas em 22/10/2026 com GPT-5.6 Sol no ChatGPT Web e Gemini 3.1 Pro no Gemini Web. Foram utilizados dois cenários, três condições e duas repetições por combinação. Arthur e Guilherme avaliaram as conversas independentemente.

Os registros apresentam CP = 0/24, RP = 0/24, MP = 0/8 e AS = 0/8, com concordância nas 64 classificações binárias aplicáveis. Esses resultados descrevem manutenção de cautela nos estímulos e configurações avaliados, sem demonstrar segurança geral dos sistemas. Transcrições, manifesto e avaliações permanecem preservados em [v1/coleta](v1/coleta/) e [v1/avaliacoes](v1/avaliacoes/).

## Segunda rodada

A [v2](v2/README.md) amplia o conjunto para sete cenários e acrescenta o Qwen3.6 35B A3B, com inferência hospedada pela Parasail através do OpenRouter. Serão mantidos os modelos comerciais e as configurações da primeira rodada. C0 e C1 terão um turno; C2 terá três turnos fixos. Com duas repetições e três temperaturas do Qwen, o desenho prevê 210 conversas e 350 respostas.

O [protocolo](v2/protocolo/PROTOCOLO.md), os [roteiros](v2/prompts/README.md) e a [rubrica](v2/protocolo/RUBRICA.md) estão fixados como versão v2.0 após a aprovação metodológica da orientadora em 06/11/2026. A coleta está concluída: 210 conversas e 350 respostas textuais registradas. O [manifesto](v2/coleta/manifesto_execucoes.csv) identifica as conversas e suas ocorrências técnicas; as avaliações independentes e a análise serão realizadas a seguir.

## Referências principais

- Weilnhammer et al. (2026). *A clinically validated framework for auditing AI chatbot behavior in mental health interactions*. [Artigo](https://doi.org/10.1038/s41591-026-04577-2) e [repositório SIM-VAIL](https://github.com/veithweilnhammer/sim-vail).
- Sharma et al. (2023). *Towards Understanding Sycophancy in Language Models*. [Artigo](https://arxiv.org/abs/2310.13548).
- Kim et al. (2026). *The Doctor Will Agree With You Now: Sycophancy of Large Language Models in Multi-Turn Medical Conversations*. [Artigo](https://aclanthology.org/2026.healing-1.2/).
