# Power BI — piloto de emprego formal (2025)

Este diretório contém o kit inicial para construir no Power BI Desktop um dashboard comparando admissões, desligamentos e saldo de empregos formais em Lucas do Rio Verde, Sorriso e Nova Mutum.

> **Importante sobre a qualidade dos dados:** a base é secundária e exploratória. Ela declara o Novo CAGED/MTE como fonte original, mas ainda precisa ser reconciliada com os microdados oficiais. Não use os valores como estatísticas oficiais definitivamente validadas.

## Arquivos

- [Medidas DAX iniciais e intermediárias](medidas_emprego.dax): oito medidas para criar no modelo.
- [Guia de interpretação das medidas DAX](dax_explicadas.md): o que cada medida calcula, como conferir os resultados e quais são suas limitações.
- [Prévia visual do dashboard](dashboard_preview.svg): ilustração estática da composição sugerida, não uma captura do Power BI.
- Base de entrada: [caged_resumo_municipal_2025_secundario.csv](../data/processed/caged_resumo_municipal_2025_secundario.csv).

## Como montar no Power BI Desktop

1. Baixe ou clone este repositório e abra o Power BI Desktop.
2. Vá em **Página Inicial → Obter dados → Texto/CSV** e selecione `data/processed/caged_resumo_municipal_2025_secundario.csv`.
3. Selecione **Transformar dados** e confira os tipos:
   - `municipio`: Texto
   - `ano`, `admissoes`, `desligamentos`, `saldo`: Número inteiro
   - `populacao_estimada`: Número inteiro
4. No Power Query, renomeie a consulta/tabela para **Emprego** e selecione **Fechar e aplicar**.
5. Na exibição **Relatório**, escolha **Modelagem → Nova medida**. Crie as medidas uma por uma copiando a fórmula correspondente do arquivo `medidas_emprego.dax`; não cole todas as medidas em uma única definição.
6. Adicione cartões para **Total de Admissões**, **Total de Desligamentos** e **Saldo Calculado**.
7. Adicione um gráfico de barras: categoria/eixo `municipio` e valor `Saldo Calculado`. Ordene pelo saldo em ordem decrescente.
8. Adicione uma segmentação de dados com `municipio`, para filtrar os visuais.
9. Para mostrar qualidade dos dados, adicione um cartão para **Diferença entre Saldo Informado e Calculado**. Zero indica que a coluna de saldo dessa base coincide com a subtração das admissões e dos desligamentos; isso não comprova que a fonte secundária esteja reconciliada com o MTE.
10. Inclua no rodapé ou subtítulo: **“Piloto exploratório — fonte secundária; pendente de validação com microdados oficiais do Novo CAGED.”**

## Valores de referência para conferir a importação

Com os três municípios selecionados, a base atual deve mostrar:

| Indicador | Valor exploratório de 2025 |
|---|---:|
| Total de admissões | 77.514 |
| Total de desligamentos | 74.163 |
| Saldo calculado | +3.351 |
| Municípios no recorte | 3 |

Saldo por município, nesta base exploratória: Lucas do Rio Verde (+1.803), Sorriso (+871) e Nova Mutum (+677). Esses valores são referências para conferir o cálculo, não estatísticas oficiais reconciliadas.

## Como interpretar as medidas

- **Saldo Calculado:** admissões menos desligamentos dentro do filtro atual. É fluxo líquido de movimentações, não estoque total de empregos nem número de pessoas desempregadas.
- **Diferença entre Saldo Informado e Calculado:** verificação aritmética da própria base; não verifica divergências contra fontes externas.
- **Admissões por 1.000 Habitantes:** indicador descritivo calculado como admissões divididas pela população estimada, multiplicado por 1.000. Não é uma taxa oficial de contratação.
- **Participação no Saldo Total (%):** parcela do saldo calculado do município no total dos municípios visíveis, preservando outros filtros aplicados ao relatório. Se o total do saldo for zero, a medida retorna em branco.

## Cuidados metodológicos

- A base atual tem uma linha por município para 2025. A medida de admissões por 1.000 habitantes assume essa granularidade. Se forem adicionados vários anos com população repetida, a modelagem populacional deve ser revista para não somar a população várias vezes.
- A tabela setorial está em outro arquivo e tem outra granularidade. Não a relacione de maneira que replique os totais municipais. Para uma análise setorial consistente, defina um modelo com dimensão de municípios e tabelas de fatos separadas ou una dados apenas após verificar chaves e granularidade.
- Não trate saldo de movimentações como estoque de empregos.
- Não apresente dados secundários como oficiais antes da reconciliação com os microdados do MTE.
- O valor do salário médio de admissão da base é específico de admissões, não o salário médio de todos os trabalhadores.

## O que ainda não está incluído

Este kit contém medidas, dados de entrada, instruções e uma prévia visual. **Ainda não inclui um arquivo `.pbix` criado e validado no Power BI Desktop.** A prévia SVG não substitui o relatório interativo.
