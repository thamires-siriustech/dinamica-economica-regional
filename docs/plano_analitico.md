# Plano analítico

## Pergunta principal

Como evoluem a produção agrícola e o mercado de trabalho formal de Lucas do Rio Verde em comparação com Sorriso e Nova Mutum?

## Etapa 1 — preparar os dados

1. Coletar PAM da API SIDRA e guardar resposta bruta com data e parâmetros.
2. Confirmar cobertura municipal, anos, produtos, variáveis, unidades e ausência de dados.
3. Reconciliar os indicadores agrícolas secundários com a extração oficial antes de considerá-los definitivos.
4. Obter e validar microdados oficiais do Novo CAGED; documentar versão, competências e layout.

## Etapa 2 — indicadores

- Área plantada/colhida, produção, rendimento e valor nominal por produto.
- Variação ano a ano apenas quando períodos consecutivos, unidades e séries comparáveis estiverem disponíveis.
- Admissões, desligamentos e saldo de emprego por mês, município e setor, com verificações de soma.
- Indicadores relativos sempre explicitando o denominador e ano de referência.

## Etapa 3 — comunicação

Primeiro relatório em Python com tabelas de qualidade e gráficos; depois dashboard no Power BI com filtros de município, período, cultura e setor. Só redigir recomendações após reconciliação das fontes.

## Limitações

Não interpretar correlação como causalidade, dados secundários como oficiais, valores nominais como crescimento real ou saldo de emprego como estoque total de trabalhadores.
