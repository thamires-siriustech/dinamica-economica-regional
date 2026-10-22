# Estratégia de portfólio para vagas de Dados e BI

**Atualizado em:** 21 de outubro de 2026  
**Objetivo profissional:** preparar evidências práticas para vagas de Analista de Dados Júnior, Analista de BI Júnior e posições remotas de dados compatíveis com o nível atual.

## 1. O que a amostra de vagas indica

Foi feita uma consulta exploratória a anúncios publicados ou atualizados em setembro e outubro de 2026. A amostra não representa estatisticamente todo o mercado, mas permite identificar sinais concretos para orientar o portfólio.

| Competência | Evidência observada em anúncios | Prioridade no portfólio |
|---|---|---|
| SQL | Vagas júnior remotas da Afya e da nstech mencionam consultas para extração e análise; outras vagas pedem consultas mais complexas. | **Muito alta** |
| Power BI e DAX | A vaga júnior remota da Afya menciona dashboards e medidas DAX básicas. Vagas de BI também pedem modelagem e DAX. | **Muito alta** |
| Qualidade e validação | Anúncios júnior citam integridade, inconsistências e validação de dados. | **Muito alta** |
| Modelagem de dados / ETL | Aparece em vagas de inteligência de dados e BI. | **Alta** |
| Documentação e comunicação | Vagas citam documentação das transformações e tradução de necessidades de negócio em indicadores. | **Alta** |
| Python / Pandas | Aparece como requisito em algumas posições e como desejável em outras. | **Alta**, depois dos fundamentos de SQL e Power BI |
| Git / GitHub | A vaga júnior remota da Afya pede conhecimento básico de Git e cita portfólio ou projetos no GitHub. | **Alta** |
| Cloud, dbt, ferramentas específicas | Aparecem em parte dos anúncios, mas variam conforme a empresa e a função. | **Depois dos fundamentos** |

### Vagas usadas como referência

- **Afya — Analista de Dados Júnior, remoto**, anúncio atualizado em 28/09/2026. Cita SQL, Power BI com DAX básico, Git, documentação e qualidade dos dados; Python aparece como desejável: https://remotar.com.br/job/164555/afya/analista-de-dados-junior
- **nstech — Analista de Dados Jr, remoto**, anúncio atualizado em 02/09/2026. Destaca consultas SQL, extração de dados, relatórios e manutenção de dashboards no Power BI: https://remotar.com.br/job/161436/nstech/analista-de-dados-jr
- **Digix — Analista de Inteligência de Dados Júnior, remoto**, anúncio atualizado em 07/10/2026. Cita SQL, modelagem, ETL, ferramentas de BI, análise descritiva/diagnóstica, qualidade e documentação: https://remotar.com.br/job/165600
- **AB InBev — Mid Level Data Analyst, remoto no Brasil**, anúncio publicado recentemente. Destaca análise de negócio, SQL, modelos semânticos e dashboards Power BI; serve como referência complementar, não como vaga de entrada: https://job-boards.greenhouse.io/abinbev/jobs/8675651002

**Interpretação:** DAX é valioso para vagas que usam Power BI, mas não se deve concluir que todas ou a maioria de todas as vagas de analista de dados exige DAX. Os requisitos mudam conforme o foco da vaga. A estratégia é construir uma base transferível e demonstrar DAX no projeto de BI.

## 2. Como aplicar a metodologia aprendida na TripleTen

A estrutura abaixo segue um fluxo de análise de ponta a ponta, alinhado aos temas descritos no currículo público da TripleTen: entender o problema de negócio, preparar os dados, analisá-los, usar SQL, criar visualizações/medidas e comunicar conclusões.

1. **Problema de negócio:** formular a pergunta que a análise deve responder e identificar quem usará o resultado.
2. **Dados e proveniência:** descrever as fontes, o período, as unidades, a granularidade e eventuais restrições de uso.
3. **Preparação:** verificar tipos, valores ausentes, duplicidades, consistência, unidades e chaves; documentar as decisões de limpeza.
4. **Análise exploratória:** calcular estatísticas descritivas, investigar padrões e verificar hipóteses sem pressupor a conclusão.
5. **SQL:** demonstrar filtros, agregações, JOINs e consultas que respondem a perguntas concretas.
6. **Modelagem e Power Query:** estruturar as tabelas e descrever as transformações necessárias.
7. **DAX e Power BI:** documentar as medidas, suas definições, o contexto de filtro e como os visuais apoiam a decisão.
8. **Conclusões e recomendações:** distinguir achados sustentados pelos dados de hipóteses e limitações.
9. **Reprodutibilidade:** organizar arquivos, instruções, dependências, testes e histórico de versões.
10. **Comunicação:** escrever um resumo executivo em linguagem simples, com as principais implicações para a tomada de decisão.

Referência curricular pública da TripleTen: https://tripleten.com/data-analytics/

Esta organização é a nossa síntese de boas práticas baseada nos tópicos públicos do currículo. Ao incorporar trabalhos do curso, preservaremos sua autoria e suas regras acadêmicas; projetos novos devem ser desenvolvidos e compreendidos por você, para que consiga explicar as escolhas numa entrevista.

## 3. Plano de melhoria do portfólio

### Projeto A — Dinâmica Econômica Regional (projeto atual)

**Ponto forte:** permite demonstrar Python, Pandas, SQL, qualidade de dados e Power BI num problema regional concreto.

**Pendência crítica:** as bases de produção agrícola e de emprego usadas no piloto ainda são secundárias e não foram reconciliadas linha a linha com os dados oficiais. Enquanto essa validação não ocorrer, os resultados precisam permanecer explicitamente exploratórios. Não publicar conclusões finais como se fossem estatísticas oficiais confirmadas.

**Próximas entregas:**
- Validar e documentar a origem dos dados;
- registrar checagens de qualidade;
- definir medidas e regras de negócio para o modelo;
- finalizar as medidas DAX com uma base apropriada;
- criar o arquivo PBIX no Power BI Desktop;
- adicionar capturas reais do relatório, metodologia e conclusões após a validação.

### Projeto B — Dashboard de negócio com DAX demonstrável

Desenvolver um caso bem delimitado de análise de vendas, atendimento ou operação usando dados públicos ou um conjunto sintético claramente identificado. O objetivo será criar um artefato reproduzível onde seja possível avaliar:
- modelo de dados e relacionamentos;
- medidas DAX (SUM, DISTINCTCOUNT, DIVIDE e CALCULATE);
- indicadores com definições de negócio;
- filtros funcionando como esperado;
- SQL para responder às perguntas de análise;
- limpeza/EDA documentada em Python ou planilha, se fizer sentido para a base.

Dados sintéticos podem ser usados para demonstrar a lógica técnica, desde que isso seja informado e nenhuma conclusão sobre uma empresa real seja atribuída a eles.

### Projeto C — Estudo de análise em Python e SQL

Criar um estudo que demonstre tratamento de dados, consultas SQL, análise exploratória, visualização, interpretação e recomendações. A prioridade é qualidade e profundidade, não quantidade de repositórios.

## 4. Checklist de qualidade para cada projeto

- [ ] Pergunta de negócio clara no início do README.
- [ ] Fonte, período, licenciamento e limitações documentados.
- [ ] Dicionário de dados com colunas, tipos e unidades.
- [ ] Limpeza e validações explicadas, não apenas executadas.
- [ ] Consultas SQL úteis, com filtros, JOINs e agregações quando pertinentes.
- [ ] Medidas DAX nomeadas, documentadas e conferidas com cálculos independentes.
- [ ] Dashboard legível, com títulos, unidades, filtros e período.
- [ ] Resultados respondem à pergunta de negócio e não extrapolam o que os dados sustentam.
- [ ] Instruções para reproduzir e estrutura organizada no GitHub.
- [ ] Um resumo executivo e tópicos para explicar o projeto numa entrevista.

## 5. Prioridades de estudo

1. **Agora:** SQL analítico, DAX básico, modelagem do Power BI, validação de dados e estrutura de um projeto de ponta a ponta.
2. **Em seguida:** DAX com CALCULATE e contexto de filtro, Power Query, modelagem dimensional e melhoria do dashboard.
3. **Depois:** aprofundar Python/Pandas, testes, Git e, conforme as vagas-alvo escolhidas, introduzir dbt, BigQuery ou outro ambiente de dados.

## 6. Como medir a evolução

Não medir a evolução apenas por quantidade de commits ou ferramentas citadas. Para cada competência, registrar:
- onde ela foi usada no projeto;
- qual problema resolveu;
- como o resultado foi conferido;
- como a decisão pode ser explicada sem consultar o código.

O objetivo é estar preparada para demonstrar o raciocínio em entrevista técnica, e não apenas declarar familiaridade com uma tecnologia.
