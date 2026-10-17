# Dicionário de dados

## PAM normalizada (`data/processed/pam_municipal_tratada.csv`)

| Campo | Significado |
|---|---|
| `codigo_ibge` | Código oficial do município, preservado como texto de 7 dígitos. |
| `municipio` | Nome padronizado via `config/municipios.csv`. |
| `ano` | Ano de referência da estatística. |
| `produto` | Cultura/produto conforme classificação retornada pelo SIDRA. |
| `variavel` | Medida PAM, por exemplo área, quantidade, rendimento ou valor. |
| `valor` | Valor numérico quando interpretável; marcadores de ausência ficam nulos. |
| `valor_sidra_original` | Conteúdo original da célula SIDRA para auditoria. |
| `status_valor` | Interpretação do marcador/valor original. |
| `unidade` | Unidade declarada pelo SIDRA; obrigatória para interpretação correta. |

A granularidade esperada do coletor é município × ano × produto × variável. Unidade e código de produto devem ser inspecionados antes de agregar. O valor da produção é nominal salvo deflação explícita.

## Piloto de emprego

Arquivos com sufixo `_secundario` são transcrições de painel secundário, não microdados oficiais. `admissoes`, `desligamentos` e `saldo` são fluxos anuais divulgados pela fonte. `salario_medio_admissao_brl` não representa salário médio de todos os trabalhadores.
