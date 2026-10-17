# Fontes e limitações

## Produção agrícola

- **Fonte oficial:** IBGE/SIDRA, Produção Agrícola Municipal (PAM), tabela 1612: https://sidra.ibge.gov.br/tabela/1612
- **API:** https://apisidra.ibge.gov.br/
- A coleta inicial planeja os anos de 2015 a 2025. A resposta real deve confirmar cobertura, códigos, unidades e marcadores de ausência antes da análise.
- Em 2025 houve alterações na classificação de produtos da PAM. Não comparar composição/ranking de culturas entre anos sem revisar a continuidade das séries.
- A base secundária presente no piloto foi compilada de páginas municipais de Outras Vias que declaram IBGE/PAM como fonte original. Ainda não foi reconciliada linha a linha com SIDRA.

## Emprego formal

- **Fonte oficial prevista:** Ministério do Trabalho e Emprego, microdados RAIS/CAGED: https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/estatisticas-trabalho/microdados-rais-e-caged
- **Piloto secundário:** Mapa do Emprego/Coalize, que declara usar Novo CAGED/MTE e dados complementares do IBGE.
- Há divergência no saldo de Lucas do Rio Verde em 2025: +1.803 na página secundária e +1.767 em notícia da Prefeitura. Diferença de 36, sem causa estabelecida. Não escolher um valor sem conciliar os microdados, competências e revisões.
- O Novo CAGED mede movimentações de emprego formal celetista; não mede toda a ocupação, o desemprego total nem a qualidade do trabalho.

## Comércio exterior (extensão futura)

- Comex Stat: https://comexstat.mdic.gov.br/pt/municipio
- O dado municipal refere-se ao domicílio fiscal da empresa declarante e pode não ser o local físico de produção.

## Inferência

O cruzamento entre produção agrícola e emprego é descritivo. Coincidência temporal ou correlação não comprova causalidade. Valores monetários nominais precisam de deflator para comparações reais ao longo do tempo.
