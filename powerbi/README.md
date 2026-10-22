# Power BI — piloto de emprego formal (2025)

Este diretório contém o kit inicial para construir no Power BI Desktop um dashboard que compara admissões, desligamentos e saldo de empregos formais em Lucas do Rio Verde, Sorriso e Nova Mutum.

> **Importante sobre a qualidade dos dados:** a base usada aqui é secundária e exploratória. Ela declara o Novo CAGED/MTE como fonte original, mas ainda precisa ser reconciliada com os microdados oficiais. Não use estes valores como estatísticas oficiais definitivamente validadas.

## Arquivos

- [Medidas DAX](medidas_emprego.dax): três medidas iniciais para criar no modelo.
- [Prévia visual do dashboard](dashboard_preview.svg): ilustração estática da composição sugerida, não é uma captura do Power BI.
- Base de entrada: [caged_resumo_municipal_2025_secundario.csv](../data/processed/caged_resumo_municipal_2025_secundario.csv).

## Como montar no Power BI Desktop

1. Baixe ou clone este repositório e abra o Power BI Desktop.
2. Vá em **Página Inicial → Obter dados → Texto/CSV** e selecione `data/processed/caged_resumo_municipal_2025_secundario.csv`.
3. Selecione **Transformar dados** e confira os tipos:
   - `municipio`: Texto
   - `ano`, `admissoes`, `desligamentos`, `saldo`: Número inteiro
   - `populacao_estimada`: Número inteiro
4. No Power Query, renomeie a consulta/tabela para **Emprego** e selecione **Fechar e aplicar**.
5. Na exibição **Relatório**, selecione **Modelagem → Nova medida**. Copie uma medida por vez do arquivo `medidas_emprego.dax`, criando cada uma separadamente.
6. Adicione três cartões com **Total de Admissões**, **Total de Desligamentos** e **Saldo de Empregos**.
7. Adicione um gráfico de barras: eixo/categoria `municipio` e valor `Saldo de Empregos`. Ordene pelo saldo em ordem decrescente.
8. Opcionalmente, adicione uma segmentação de dados usando `municipio`.
9. Inclua no rodapé ou subtítulo do relatório: **“Piloto exploratório — fonte secundária; pendente de validação com microdados oficiais do Novo CAGED.”**

## Resultado esperado para conferir a importação

Com todos os três municípios selecionados, a base atual deve produzir:

| Indicador | Valor exploratório de 2025 |
|---|---:|
| Total de admissões | 77.514 |
| Total de desligamentos | 74.163 |
| Saldo calculado | +3.351 |

O saldo calculado é a diferença entre admissões e desligamentos. Por município, a base atual contém: Lucas do Rio Verde (+1.803), Sorriso (+871) e Nova Mutum (+677). Estes valores são usados apenas como conferência do exemplo e continuam sujeitos à ressalva metodológica acima.

## Dicas de apresentação

- Use títulos que indiquem a métrica e o período.
- Formate os totais com separador de milhar e o saldo com sinal positivo/negativo.
- Não trate saldo de movimentações como estoque total de empregos nem como número de desempregados.
- Esta base tem uma linha por município para o ano de 2025; ela não permite analisar tendências mensais.
- Para análise por setor, consulte também `data/processed/caged_setor_2025_secundario.csv` e modele essa granularidade separadamente para não duplicar os totais municipais.
- Antes de publicar conclusões substantivas, concilie os resultados com os microdados oficiais do MTE.

## O que ainda não está incluído

Este kit contém as medidas, dados de entrada, instruções e uma prévia visual. **Ainda não inclui um arquivo `.pbix` criado e validado no Power BI Desktop.** O arquivo do Power BI precisa ser montado e salvo no Desktop seguindo as etapas acima; a prévia SVG não substitui o relatório interativo.
