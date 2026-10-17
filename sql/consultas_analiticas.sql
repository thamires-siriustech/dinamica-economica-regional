-- Consultas PostgreSQL para usar após carregar as tabelas.
-- 1. Série histórica de quantidade produzida para soja e milho.
SELECT m.municipio, f.ano, f.produto, f.valor AS quantidade_produzida, f.unidade
FROM fact_producao_agricola f
JOIN dim_municipio m ON m.codigo_ibge = f.codigo_ibge
WHERE f.variavel ILIKE '%Quantidade produzida%'
  AND (f.produto ILIKE '%Soja%' OR f.produto ILIKE '%Milho%')
ORDER BY f.produto, m.municipio, f.ano;

-- 2. Variação percentual anual. Só calcula com anos consecutivos, unidade idêntica
-- e valores anterior/atual disponíveis; ausência não é tratada como zero.
WITH serie AS (
    SELECT f.*, LAG(f.ano) OVER w AS ano_anterior,
           LAG(f.valor) OVER w AS valor_anterior,
           LAG(f.unidade) OVER w AS unidade_anterior
    FROM fact_producao_agricola f
    WINDOW w AS (PARTITION BY f.codigo_ibge, f.produto, f.variavel ORDER BY f.ano)
)
SELECT m.municipio, s.produto, s.variavel, s.ano, s.valor,
       CASE WHEN s.ano - s.ano_anterior = 1
                 AND s.valor IS NOT NULL AND s.valor_anterior IS NOT NULL
                 AND s.unidade = s.unidade_anterior AND s.valor_anterior <> 0
            THEN 100.0 * (s.valor / s.valor_anterior - 1) END AS variacao_percentual_anual
FROM serie s JOIN dim_municipio m ON m.codigo_ibge = s.codigo_ibge
ORDER BY m.municipio, s.produto, s.variavel, s.ano;

-- 3. Saldo do piloto secundário por município. Não equivale à extração oficial do MTE.
SELECT m.municipio, f.ano, f.admissoes, f.desligamentos, f.saldo_reportado,
       f.salario_medio_admissao_brl,
       1000.0 * f.saldo_reportado / NULLIF(f.populacao_estimada, 0) AS saldo_por_mil_habitantes
FROM fact_caged_resumo_anual_piloto f
JOIN dim_municipio m ON m.codigo_ibge = f.codigo_ibge
WHERE f.ano = 2025 ORDER BY f.saldo_reportado DESC;

-- 4. Saldo por setor, mantendo a fonte.
SELECT m.municipio, f.ano, f.setor_agregado, f.admissoes, f.desligamentos, f.saldo, f.fonte
FROM fact_caged_setor_anual_piloto f
JOIN dim_municipio m ON m.codigo_ibge = f.codigo_ibge
WHERE f.ano = 2025 ORDER BY m.municipio, f.saldo DESC;
