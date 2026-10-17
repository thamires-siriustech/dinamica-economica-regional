"""Gera tabelas analíticas e gráficos a partir da base PAM normalizada.

Execute depois de python src/collect_pam.py: python src/analyze_pam.py.
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "municipios.csv"
INPUT_PATH = ROOT / "data" / "processed" / "pam_municipal_tratada.csv"
OUTPUT_DIR = ROOT / "reports" / "outputs"
FIGURE_DIR = ROOT / "reports" / "figures"

REQUIRED_COLUMNS = {
    "codigo_ibge", "municipio", "ano", "produto", "variavel", "valor",
    "valor_sidra_original", "status_valor", "unidade",
}
TARGET_CROPS = {
    "soja": re.compile(r"\bsoja\s*\(em grao\)", flags=re.IGNORECASE),
    "milho": re.compile(r"\bmilho\s*\(em grao\)", flags=re.IGNORECASE),
}


def simplify(value: object) -> str:
    text = unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", text).strip().casefold()


def normalize_label(series: pd.Series) -> pd.Series:
    return series.fillna("").astype(str).map(simplify)


def load_processed(path: Path = INPUT_PATH) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Base tratada não encontrada: {path}. Execute primeiro python src/collect_pam.py.")
    df = pd.read_csv(path, dtype={"codigo_ibge": str})
    missing = sorted(REQUIRED_COLUMNS - set(df.columns))
    if missing:
        raise ValueError(f"A base tratada não contém as colunas obrigatórias: {missing}")
    df["codigo_ibge"] = df["codigo_ibge"].astype(str).str.zfill(7)
    df["ano"] = pd.to_numeric(df["ano"], errors="coerce")
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    df = df.dropna(subset=["codigo_ibge", "ano", "produto", "variavel"]).copy()
    df["ano"] = df["ano"].astype(int)
    df["produto_norm"] = normalize_label(df["produto"])
    df["variavel_norm"] = normalize_label(df["variavel"])
    key = ["codigo_ibge", "ano", "produto", "variavel"]
    duplicated = df.duplicated(key, keep=False)
    if duplicated.any():
        sample = df.loc[duplicated, key].head(8).to_dict("records")
        raise ValueError(f"Há chaves duplicadas na base processada. Exemplos: {sample}")
    return df


def is_crop(df: pd.DataFrame, crop: str) -> pd.Series:
    source = df["produto_norm"] if "produto_norm" in df.columns else normalize_label(df["produto"])
    return source.fillna("").astype(str).str.contains(TARGET_CROPS[crop], na=False)


def latest_common_year(df: pd.DataFrame, variable_pattern: str, product_pattern: str | None = None,
                       municipalities: Iterable[str] | None = None) -> int | None:
    subset = df[df["valor"].notna() & df["variavel_norm"].str.contains(simplify(variable_pattern), regex=False)].copy()
    if product_pattern is not None:
        subset = subset[subset["produto"].astype(str).str.contains(product_pattern, case=False, regex=True, na=False)]
    if municipalities is not None:
        subset = subset[subset["municipio"].isin(list(municipalities))]
    names = list(municipalities) if municipalities is not None else sorted(subset["municipio"].dropna().unique())
    if len(names) < 2:
        return None
    years_by_city = [set(subset.loc[subset["municipio"].eq(name), "ano"].astype(int)) for name in names]
    common = set.intersection(*years_by_city) if years_by_city else set()
    return max(common) if common else None


def build_coverage_report(df: pd.DataFrame) -> pd.DataFrame:
    config = pd.read_csv(CONFIG_PATH, dtype={"codigo_ibge": str})
    out = []
    for expected in config.to_dict(orient="records"):
        city = expected["municipio"]
        group = df.loc[df["municipio"].eq(city)]
        years = sorted(group["ano"].dropna().astype(int).unique().tolist())
        out.append({
            "municipio": city, "codigo_ibge": str(expected["codigo_ibge"]).zfill(7),
            "papel": expected.get("papel", ""), "presente_na_extracao": not group.empty,
            "ano_inicial": min(years) if years else None, "ano_final": max(years) if years else None,
            "quantidade_anos": len(years), "anos_observados": ", ".join(map(str, years)),
            "produtos_distintos": int(group["produto"].nunique()),
            "variaveis_distintas": int(group["variavel"].nunique()), "linhas": int(len(group)),
            "valores_numericos": int(group["valor"].notna().sum()),
            "marcadores_nao_numericos": int(group["valor"].isna().sum()),
        })
    return pd.DataFrame(out).sort_values("municipio").reset_index(drop=True)


def build_yoy_table(df: pd.DataFrame) -> pd.DataFrame:
    cols = ["codigo_ibge", "municipio", "produto", "variavel", "unidade", "ano", "valor", "status_valor"]
    base = df[cols].copy()
    prior = base[["codigo_ibge", "produto", "variavel", "unidade", "ano", "valor"]].copy()
    prior["ano"] = prior["ano"] + 1
    prior = prior.rename(columns={"valor": "valor_ano_anterior", "unidade": "unidade_ano_anterior"})
    merged = base.merge(prior, on=["codigo_ibge", "produto", "variavel", "ano"], how="left", validate="one_to_one")
    unit_match = merged["unidade"].fillna("").eq(merged["unidade_ano_anterior"].fillna("")) & merged["unidade"].notna()
    valid_pair = merged["valor_ano_anterior"].notna() & merged["valor"].notna() & unit_match
    merged["variacao_absoluta"] = pd.NA
    merged.loc[valid_pair, "variacao_absoluta"] = merged.loc[valid_pair, "valor"] - merged.loc[valid_pair, "valor_ano_anterior"]
    valid_pct = valid_pair & merged["valor_ano_anterior"].ne(0)
    merged["variacao_percentual"] = pd.NA
    merged.loc[valid_pct, "variacao_percentual"] = (merged.loc[valid_pct, "valor"] / merged.loc[valid_pct, "valor_ano_anterior"] - 1) * 100
    merged["comparabilidade_anual"] = "sem valor comparável para o ano anterior"
    both_values = merged["valor_ano_anterior"].notna() & merged["valor"].notna()
    merged.loc[both_values & ~unit_match, "comparabilidade_anual"] = "unidade diferente entre anos"
    merged.loc[valid_pair, "comparabilidade_anual"] = "comparável com ano anterior"
    merged.loc[valid_pair & merged["valor_ano_anterior"].eq(0), "comparabilidade_anual"] = "variação percentual indefinida: valor anterior zero"
    return merged.sort_values(["municipio", "produto", "variavel", "ano"]).reset_index(drop=True)


def build_core_crops(df: pd.DataFrame) -> pd.DataFrame:
    crop_mask = is_crop(df, "soja") | is_crop(df, "milho")
    out = df.loc[crop_mask].copy()
    out = out[~out["produto_norm"].isin(["total", "total geral"])].copy()
    keep_vars = {"quantidade produzida", "area plantada", "area colhida", "rendimento medio da producao", "rendimento medio", "valor da producao"}
    out = out[out["variavel_norm"].isin(keep_vars)]
    out["cultura_resumida"] = out["produto"].apply(lambda value: "Soja" if "soja" in str(value).casefold() else "Milho")
    return out[["codigo_ibge", "municipio", "ano", "cultura_resumida", "produto", "variavel", "valor", "valor_sidra_original", "status_valor", "unidade"]].sort_values(["cultura_resumida", "municipio", "ano", "variavel"]).reset_index(drop=True)


def build_latest_value_ranking(df: pd.DataFrame) -> tuple[pd.DataFrame, int | None]:
    values = df.loc[df["variavel_norm"].eq("valor da producao") & df["valor"].notna()].copy()
    values = values[~values["produto_norm"].isin(["total", "total geral"])].copy()
    configured_cities = pd.read_csv(CONFIG_PATH)["municipio"].astype(str).tolist()
    year = latest_common_year(values, "valor da producao", municipalities=configured_cities)
    if year is None:
        return pd.DataFrame(columns=["codigo_ibge", "municipio", "ano", "produto", "valor", "unidade", "posicao"]), None
    latest = values[values["ano"].eq(year)].copy().sort_values(["municipio", "valor"], ascending=[True, False])
    latest["posicao"] = latest.groupby("municipio").cumcount() + 1
    latest["ano"] = year
    return latest[["codigo_ibge", "municipio", "ano", "produto", "valor", "unidade", "posicao"]].reset_index(drop=True), year


def plot_crop_trend(core: pd.DataFrame, crop: str, variable_fragment: str) -> str | None:
    crop_key = "soja" if crop.casefold() == "soja" else "milho"
    subset = core[core["cultura_resumida"].str.casefold().eq(crop_key)].copy()
    subset = subset[subset["variavel"].map(simplify).str.contains(simplify(variable_fragment), regex=False) & subset["valor"].notna()]
    if subset.empty:
        return None
    units = sorted(subset["unidade"].dropna().astype(str).unique().tolist())
    if len(units) > 1:
        print(f"Gráfico não gerado para {crop}/{variable_fragment}: unidades diferentes {units}.", file=sys.stderr)
        return None
    fig, ax = plt.subplots(figsize=(10, 5.5))
    for city, group in subset.groupby("municipio"):
        group = group.sort_values("ano")
        ax.plot(group["ano"], group["valor"], marker="o", label=city)
    ax.set_title(f"{variable_fragment} — {crop.title()} por município")
    ax.set_xlabel("Ano")
    ax.set_ylabel(f"{variable_fragment} ({units[0] if units else 'unidade não informada'})")
    ax.grid(alpha=0.25)
    ax.legend()
    fig.tight_layout()
    filename = f"{crop_key}_{simplify(variable_fragment).replace(' ', '_')}_por_municipio.png"
    out = FIGURE_DIR / filename
    fig.savefig(out, dpi=160, bbox_inches="tight")
    plt.close(fig)
    try:
        return str(out.relative_to(ROOT))
    except ValueError:
        return str(out)


def generate_outputs(df: pd.DataFrame) -> dict:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    coverage, yoy, core = build_coverage_report(df), build_yoy_table(df), build_core_crops(df)
    ranking, ranking_year = build_latest_value_ranking(df)
    coverage.to_csv(OUTPUT_DIR / "cobertura_por_municipio.csv", index=False, encoding="utf-8-sig")
    yoy.to_csv(OUTPUT_DIR / "variacao_anual.csv", index=False, encoding="utf-8-sig")
    core.to_csv(OUTPUT_DIR / "soja_milho_indicadores.csv", index=False, encoding="utf-8-sig")
    ranking.to_csv(OUTPUT_DIR / "ranking_valor_producao.csv", index=False, encoding="utf-8-sig")
    figure_paths = []
    for crop in ("Soja", "Milho"):
        for variable in ("Quantidade produzida", "Rendimento médio"):
            plot = plot_crop_trend(core, crop, variable)
            if plot:
                figure_paths.append(plot)
    metadata = {
        "input": str(INPUT_PATH.relative_to(ROOT)),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "rows_in_input": int(len(df)),
        "municipalities": sorted(df["municipio"].dropna().unique().tolist()),
        "years_available": sorted(int(y) for y in df["ano"].unique()),
        "latest_common_year_for_value_ranking": ranking_year,
        "outputs": ["reports/outputs/cobertura_por_municipio.csv", "reports/outputs/variacao_anual.csv",
                    "reports/outputs/soja_milho_indicadores.csv", "reports/outputs/ranking_valor_producao.csv", *figure_paths],
        "interpretation_notes": [
            "Variação anual exige observações nos dois anos e unidade idêntica.",
            "Ausência de observação não é convertida em zero.",
            "Valor da produção é nominal e não foi deflacionado.",
            "Mudanças na classificação da PAM em 2025 exigem cautela ao comparar composição de culturas.",
        ],
    }
    (OUTPUT_DIR / "metadados_analise.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    return metadata


def main() -> int:
    try:
        metadata = generate_outputs(load_processed())
    except (FileNotFoundError, ValueError, OSError, KeyError) as exc:
        print(f"Não foi possível executar a análise: {exc}", file=sys.stderr)
        return 1
    print("Análise concluída.")
    print(f"Registros: {metadata['rows_in_input']:,}")
    print(f"Municípios: {', '.join(metadata['municipalities'])}")
    print(f"Anos: {metadata['years_available']}")
    print(f"Ano comum para ranking: {metadata['latest_common_year_for_value_ranking']}")
    for path in metadata["outputs"]:
        print(f" - {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
