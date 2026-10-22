# Dinâmica Econômica Regional: Lucas do Rio Verde e entorno

**Status:** versão inicial de portfólio publicada; pipeline de coleta e análise preparado. Os resultados numéricos atuais são exploratórios e ainda dependem de reconciliação com as fontes oficiais.

## Objetivo

Investigar a evolução da produção agrícola e do mercado de trabalho formal em Lucas do Rio Verde (MT), usando Sorriso e Nova Mutum como referências comparativas. O projeto combina Python, Pandas, SQL e documentação para uma futura apresentação em Power BI.

As análises descrevem tendências; não presumem que o agronegócio, por si só, explique mudanças no emprego. Correlação temporal não será interpretada como causalidade.

## Perguntas de negócio

1. Quais culturas concentram produção e valor de produção em cada município?
2. Como evoluem área plantada, volume produzido e rendimento médio?
3. Quais setores registram os maiores saldos de emprego formal?
4. As mudanças na produção agrícola e no emprego ocorrem em períodos semelhantes?
5. Em quais indicadores Lucas do Rio Verde se diferencia de Sorriso e Nova Mutum?

## Municípios

| Município | Código IBGE |
|---|---:|
| Lucas do Rio Verde | 5105259 |
| Sorriso | 5107925 |
| Nova Mutum | 5106224 |

## Fontes

- **IBGE/SIDRA — PAM, tabela 1612:** https://sidra.ibge.gov.br/tabela/1612
- **API SIDRA:** https://apisidra.ibge.gov.br/
- **MTE — microdados RAIS e CAGED:** https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/estatisticas-trabalho/microdados-rais-e-caged
- **Comex Stat (extensão futura):** https://comexstat.mdic.gov.br/pt/municipio

### Limitações atuais

A coleta direta da PAM pela API SIDRA precisa ser executada e validada em ambiente com acesso à API. A base agrícola de 66 registros incluída no piloto foi transcrita de páginas secundárias que declaram o IBGE/PAM como fonte original; ela ainda não foi reconciliada linha a linha com o SIDRA.

O piloto de emprego formal de 2025 também usa páginas secundárias que declaram utilizar o Novo CAGED/MTE. Há uma divergência de saldo para Lucas do Rio Verde (+1.803 no painel secundário e +1.767 em notícia da Prefeitura). A diferença está documentada em `data/processed/auditoria_fontes_saldo_lucas_2025.csv`; sua causa ainda não foi estabelecida.

Essas bases são exploratórias e não devem ser apresentadas como extrações oficiais já validadas. Os números, fontes e limitações estão descritos nos relatórios em `reports/outputs/` e nos documentos de `docs/`.

## Estratégia de portfólio para vagas de dados

Consulte o [plano de portfólio alinhado a vagas de Dados e BI](docs/portfolio_roadmap.md), que resume competências observadas em anúncios remotos, uma metodologia de ponta a ponta, projetos prioritários e um checklist de qualidade.

## Kit inicial de Power BI

Adicionei uma pasta `powerbi/` com medidas DAX, instruções para importar a base e montar os visuais, e uma prévia estática de layout:

- [Guia para montar o dashboard no Power BI Desktop](powerbi/README.md)
- [Medidas DAX iniciais](powerbi/medidas_emprego.dax)
- [Explicação e validação das medidas DAX](powerbi/dax_explicadas.md)
- [Prévia visual estática do dashboard](powerbi/dashboard_preview.svg)

O kit usa os dados secundários de emprego de 2025 já documentados neste projeto. **Ainda não contém um arquivo `.pbix` criado e validado no Power BI Desktop.** A prévia SVG serve apenas para ilustrar a composição pretendida, e os valores devem continuar rotulados como exploratórios até serem reconciliados com os microdados oficiais.

## Estrutura

- `config/`: municípios analisados
- `src/`: coleta, validação e análise
- `tests/`: testes offline
- `sql/`: esquema relacional e consultas analíticas
- `notebooks/`: exploração dos dados e comunicação dos resultados
- `data/processed/`: pequenas bases tratadas e pilotos com proveniência documentada
- `reports/`: tabelas derivadas e gráficos
- `docs/`: fontes, dicionário de dados, plano de análise e proposta para Power BI
- `powerbi/`: medidas DAX, guia de montagem e prévia estática do dashboard

## Como executar

Requer Python 3.10 ou superior.

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m unittest discover -s tests -v
python src/collect_pam.py
python src/analyze_pam.py
```

Em Windows PowerShell, também é possível executar `powershell -ExecutionPolicy Bypass -File .\scripts\executar_pipeline.ps1`. A análise da PAM só deve ser executada após uma coleta oficial válida.

A base secundária pode ser reproduzida separadamente com:

```bash
python src/analyze_secondary_pilot.py
```

Essa etapa não consulta a internet e não converte dados secundários em dados oficiais.

## Princípios de qualidade

- Manter respostas brutas separadas dos dados transformados.
- Registrar fonte, período, unidade e filtros.
- Não substituir valores ausentes por zero.
- Não misturar produtos ou unidades de medida diferentes.
- Ajustar valores monetários pela inflação antes de interpretar variações de longo prazo em termos reais.
- Separar observações, hipóteses e conclusões causais.
- Não publicar microdados restritos ou dados pessoais identificáveis.

## Próximas etapas

1. Executar e conferir a coleta oficial da PAM.
2. Conciliar a série de emprego com microdados oficiais do MTE.
3. Harmonizar as séries temporal e metodologicamente.
4. Construir e salvar o arquivo interativo no Power BI Desktop após validar os dados.
