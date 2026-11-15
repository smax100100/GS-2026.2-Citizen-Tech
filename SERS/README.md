Markdown
#  Módulo de Mobilidade Sustentável e Energia (SERS)

Contribuição da disciplina Soluções em Energias Renováveis e Sustentáveis (FIAP — 1CC / GS 2026.2) integrada ao assistente digital. 

Integrantes do Grupo
Heitor Máximus Mucha — RM: 571407

Andrei Henrique Santos — RM: 569440 


---

## Descrição do Público e do Problema
* Público-alvo: Cidadãos urbanos (trabalhadores e estudantes) que realizam deslocamentos diários pendulares na cidade (referência de $20\text{ km/dia}$ ida e volta, $22\text{ dias úteis/mês}$) e utilizam o **Mobi AI** para decidir rotas, direitos no trânsito e modais de transporte.
* Problema abordado: A dependência do automóvel individual movido a combustível fóssil gera alto gasto mensal com abastecimento, baixa eficiência energética por passageiro transportado, congestionamentos e elevadas emissões de gases de efeito estufa ($CO_2$), agravados pela falta de comparação clara entre transporte coletivo e micromobilidade elétrica alimentada por fonte renovável.
* Como a solução contribui: O módulo de energia do **Mobi Ai** compara custo energético, consumo ($kWh$), retorno financeiro (*payback*) e emissões de $CO_2$ entre modais urbanos, orientando o cidadão sobre a melhor alternativa conforme distância, infraestrutura cicloviária e orçamento, além de informar regras do CTB e limitações técnicas.

---

## Funcionalidades de Energia Incorporadas ao RotaCidadã
1. Comparativo Energético de Modais Urbanos: Analisa, para a mesma necessidade de deslocamento ($440\text{ km/mês}$ / $5.280\text{ km/ano}$), o carro a combustão (cenário base), o transporte público coletivo (eficiência por passageiro) e a bicicleta elétrica (E-Bike $350\text{ W}$) recarregada via energia solar fotovoltaica (fonte renovável).
2. **Simulador de Trajeto do Cidadão:** Permite inserir a distância diária ($km$), dias úteis no mês e preço local da gasolina ($R\$/L$) para recalcular gastos, economia e emissões evitadas.
3. **Recomendação Contextualizada por Perfil:** Cruza disponibilidade de ciclovia/bicicletário, distância máxima e orçamento para indicar a alternativa mais viável, lembrando deveres de segurança viária (CTB).
4. **Transparência, Fontes e Limitações:** Exibe referências técnicas verificáveis e avisos explícitos de que estimativas de custo, geração solar e economia não são resultados garantidos.

---

## Instruções para Executar e Testar a Solução

### Pré-requisitos
* **Python 3.10+** (utiliza apenas biblioteca padrão: `dataclasses`, `typing`, `sys`).

### Execução do Assistente (Modo Interativo)
```bash
git clone <https://github.com/smax100100/GS-2026.2-Citizen-Tech>
cd <smax100100/GS-2026.2-Citizen-Tech>
python src/sers_mobilidade.py
