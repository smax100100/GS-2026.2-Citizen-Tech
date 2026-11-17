# Citizen Assist AI - Despachante Digital de Trânsito

Assistente digital desenvolvido em Python para o desafio **CitizenTech** (GS 2026.2 - FIAP), focado em orientar condutores e proprietários de veículos sobre serviços do Detran, CNH, licenciamento, infrações e transferência veicular com base em fontes oficiais e sem coleta de dados pessoais.

## Integrantes

- Andrei Henrique Santos - RM 569440
- Heitor Maxímus Mucha - RM 571407

## Participantes
- **Participantes:** 3 usuários externos de diferentes faixas etárias (adultos e idoso), sem coleta de identificação.

## Público e Problema Escolhido

- **Público:** Motoristas, proprietários de veículos e cidadãos que precisam realizar serviços de trânsito.
- **Problema:** Dificuldade em localizar quais documentos levar, onde realizar procedimentos (Detran, Poupatempo, CDT) e como evitar golpes ou sites não oficiais.

## ODS Relacionados

- **ODS 11 (Cidades e Comunidades Sustentáveis):** Facilita o acesso à mobilidade e serviços urbanos.
- **ODS 16 (Paz, Justiça e Instituições Eficazes):** Promove transparência e acesso público a informações institucionais.


## Regra de Pontuação Utilizada

- Normalização de texto (minúsculas, remoção de acentos e pontuação).
- **+3 pontos** por palavra-chave da orientação presente na pergunta (por substring ou correspondência completa dos termos da palavra-chave).
- **+1 ponto** por palavra da pergunta (4 letras ou mais) presente no título da orientação.
- **Confiança ALTA:** 6 pontos ou mais | **Confiança MÉDIA:** 3 a 5 pontos | **Não encontrado:** menos de 3 pontos.

## Fontes Consultadas

- Detran.SP (`[https://www.detran.sp.gov.br](https://www.detran.sp.gov.br)`)
- Poupatempo SP (`[https://www.poupatempo.sp.gov.br](https://www.poupatempo.sp.gov.br)`)
- Portal Gov.br / Ministério dos Transportes (`[https://www.gov.br/transportes](https://www.gov.br/transportes)`)

## Resultado dos Testes com Usuários

- **Total de atendimentos:** 10
- **Resposta encontrada (%):** 90.0%
- **Taxa de acerto - ajudou (%):** 80.0%
- **Tempo médio para encontrar:** 19.7s
- **Tentativas por atendimento:** 1.0
- **Facilidade de uso (1 a 5):**  5/ 5
- **Dúvidas sem solução:**
  - "como solicitar o cartao de estacionamento para idoso?"
- **Melhoria aplicada após testes:** Inclusão da orientação ID 15 (Credencial de Estacionamento para Idoso) no `data/base_conhecimento.json` com palavras-chave relacionadas ao serviço.

## Limitações

- O assistente não consulta bancos de dados reais de RENAVAM ou CNH e não substitui os canais oficiais do Detran/Gov.br.
- A busca depende da correspondência das palavras-chave cadastradas no arquivo JSON.

## Vídeo Técnico

- **Link:** ________________________________________

## Como Executar

1. Certifique-se de ter o Python 3 instalado.
2. Na raiz do projeto, execute:

```bash
python main.py
```
