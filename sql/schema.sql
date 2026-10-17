-- Esquema analítico inicial (PostgreSQL). Validar tipos após a extração oficial.
CREATE TABLE dim_municipio (
    codigo_ibge CHAR(7) PRIMARY KEY,
    municipio VARCHAR(100) NOT NULL,
    uf CHAR(2) NOT NULL,
    papel VARCHAR(30) NOT NULL
);

CREATE TABLE fact_producao_agricola (
    codigo_ibge CHAR(7) NOT NULL,
    ano SMALLINT NOT NULL,
    produto VARCHAR(150) NOT NULL,
    codigo_produto VARCHAR(30),
    variavel VARCHAR(100) NOT NULL,
    codigo_variavel VARCHAR(30),
    valor NUMERIC(24, 6),
    valor_sidra_original VARCHAR(80) NOT NULL,
    status_valor VARCHAR(60) NOT NULL,
    unidade VARCHAR(100),
    codigo_unidade VARCHAR(30),
    fonte VARCHAR(150) NOT NULL DEFAULT 'IBGE/SIDRA PAM tabela 1612',
    data_coleta TIMESTAMPTZ,
    PRIMARY KEY (codigo_ibge, ano, produto, variavel),
    FOREIGN KEY (codigo_ibge) REFERENCES dim_municipio(codigo_ibge)
);

-- Fluxo mensal do Novo CAGED. Não misturar com estoque anual da RAIS sem rotular a medida.
CREATE TABLE fact_emprego_formal_mensal (
    codigo_ibge CHAR(7) NOT NULL,
    competencia DATE NOT NULL,
    atividade_economica VARCHAR(150) NOT NULL,
    fonte VARCHAR(30) NOT NULL,
    medida VARCHAR(50) NOT NULL,
    valor NUMERIC(20, 4),
    unidade VARCHAR(100),
    data_coleta TIMESTAMPTZ,
    PRIMARY KEY (codigo_ibge, competencia, atividade_economica, fonte, medida),
    FOREIGN KEY (codigo_ibge) REFERENCES dim_municipio(codigo_ibge)
);

-- Tabelas auxiliares para o piloto secundário; não são dados oficiais reconciliados.
CREATE TABLE fact_caged_resumo_anual_piloto (
    codigo_ibge CHAR(7) NOT NULL,
    ano SMALLINT NOT NULL,
    admissoes INTEGER NOT NULL,
    desligamentos INTEGER NOT NULL,
    saldo_reportado INTEGER NOT NULL,
    salario_medio_admissao_brl NUMERIC(12,2),
    populacao_estimada INTEGER,
    fonte VARCHAR(150) NOT NULL,
    url_fonte TEXT NOT NULL,
    status_fonte VARCHAR(80) NOT NULL,
    data_coleta DATE NOT NULL,
    PRIMARY KEY (codigo_ibge, ano, fonte),
    FOREIGN KEY (codigo_ibge) REFERENCES dim_municipio(codigo_ibge),
    CHECK (saldo_reportado = admissoes - desligamentos)
);

CREATE TABLE fact_caged_setor_anual_piloto (
    codigo_ibge CHAR(7) NOT NULL,
    ano SMALLINT NOT NULL,
    setor_agregado VARCHAR(100) NOT NULL,
    admissoes INTEGER NOT NULL,
    desligamentos INTEGER NOT NULL,
    saldo INTEGER NOT NULL,
    fonte VARCHAR(150) NOT NULL,
    url_fonte TEXT NOT NULL,
    status_fonte VARCHAR(80) NOT NULL,
    data_coleta DATE NOT NULL,
    PRIMARY KEY (codigo_ibge, ano, setor_agregado, fonte),
    FOREIGN KEY (codigo_ibge) REFERENCES dim_municipio(codigo_ibge),
    CHECK (saldo = admissoes - desligamentos)
);
