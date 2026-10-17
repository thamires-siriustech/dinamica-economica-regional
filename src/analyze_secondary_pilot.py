"""Reproduz análise exploratória da base agrícola secundária do piloto.

Esta rotina NÃO transforma a base secundária em uma extração oficial do SIDRA.
Execute na raiz: python src/analyze_secondary_pilot.py
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "processed" / "pam_base_secundaria_piloto.csv"
OUT = ROOT / "reports" / "outputs"
FIG = ROOT / "reports" / "figures"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(SOURCE, encoding="utf-8-sig")
    required = {
        "codigo_ibge", "municipio", "ano", "cultura", "producao_t",
        "area_plantada_ha", "produtividade_kg_ha",
        "valor_producao_mil_reais_nominal", "status_base",
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Colunas obrigatórias ausentes: {sorted(missing)}")
    if len(df) != 66:
        raise ValueError(f"Esperadas 66 linhas (3 municípios × 2 culturas × 11 anos); recebidas {len(df)}")
    if df.duplicated(["codigo_ibge", "ano", "cultura"]).any():
        raise ValueError("Chaves duplicadas em município × ano × cultura.")
    if not df["status_base"].str.contains("validar_com_sidra", na=False).all():
        raise ValueError("Status da proveniência inesperado; revise a classificação da fonte.")
    numeric = ["ano", "producao_t", "area_plantada_ha", "produtividade_kg_ha", "valor_producao_mil_reais_nominal"]
    for col in numeric:
        df[col] = pd.to_numeric(df[col], errors="raise")
    if (df[["producao_t", "area_plantada_ha", "produtividade_kg_ha"]] < 0).any().any():
        raise ValueError("Valores negativos em medidas físicas; revise a base.")

    rows = []
    for (municipality, crop), g in df.groupby(["municipio", "cultura"], sort=True):
        g = g.sort_values("ano")
        first = g.loc[g["ano"].eq(2015)]
        last = g.loc[g["ano"].eq(2025)]
        prev = g.loc[g["ano"].eq(2024)]
        if len(first) != 1 or len(last) != 1 or len(prev) != 1:
            raise ValueError(f"Série 2015/2024/2025 incompleta para {municipality} — {crop}")
        a, b, c = first.iloc[0], last.iloc[0], prev.iloc[0]
        pct = lambda x, y: (y / x - 1) * 100 if x else float("nan")
        rows.append({
            "municipio": municipality, "cultura": crop,
            "producao_2015_t": int(a["producao_t"]), "producao_2025_t": int(b["producao_t"]),
            "variacao_producao_2015_2025_pct": round(pct(a["producao_t"], b["producao_t"]), 2),
            "area_2015_ha": int(a["area_plantada_ha"]), "area_2025_ha": int(b["area_plantada_ha"]),
            "variacao_area_2015_2025_pct": round(pct(a["area_plantada_ha"], b["area_plantada_ha"]), 2),
            "produtividade_2015_kg_ha": int(a["produtividade_kg_ha"]),
            "produtividade_2025_kg_ha": int(b["produtividade_kg_ha"]),
            "variacao_produtividade_2015_2025_pct": round(pct(a["produtividade_kg_ha"], b["produtividade_kg_ha"]), 2),
            "producao_2024_t": int(c["producao_t"]),
            "variacao_producao_2024_2025_pct": round(pct(c["producao_t"], b["producao_t"]), 2),
            "valor_producao_2025_mil_reais_nominal": int(b["valor_producao_mil_reais_nominal"]),
            "variacao_valor_nominal_2015_2025_pct": round(pct(a["valor_producao_mil_reais_nominal"], b["valor_producao_mil_reais_nominal"]), 2),
        })
    indicators = pd.DataFrame(rows).sort_values(["municipio", "cultura"])
    indicators.to_csv(OUT / "indicadores_piloto.csv", index=False, encoding="utf-8-sig")
    audit = {
        "status": "base_secundaria_piloto_nao_reconciliada_com_sidra",
        "rows": int(len(df)),
        "expected_rows": 66,
        "municipalities": sorted(df["municipio"].unique().tolist()),
        "years": sorted(int(x) for x in df["ano"].unique()),
        "crops": sorted(df["cultura"].unique().tolist()),
        "unique_keys": int(df[["codigo_ibge", "ano", "cultura"]].drop_duplicates().shape[0]),
        "source_note": "Páginas secundárias que declaram IBGE/PAM tabela 1612; validação oficial pendente.",
        "monetary_values": "nominais; não interpretar variação como crescimento real sem deflator",
    }
    (OUT / "auditoria_base_piloto.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")

    for crop, filename, ycol, ylabel in [
        ("soja", "producao_soja_2015_2025.png", "producao_t", "Produção (toneladas)"),
        ("milho em grão", "producao_milho_2015_2025.png", "producao_t", "Produção (toneladas)"),
    ]:
        fig, ax = plt.subplots(figsize=(9, 5.2))
        for municipality, g in df[df["cultura"].eq(crop)].groupby("municipio"):
            ax.plot(g.sort_values("ano")["ano"], g.sort_values("ano")[ycol], marker="o", label=municipality)
        ax.set_title(f"Produção de {crop} — base secundária exploratória")
        ax.set_xlabel("Ano")
        ax.set_ylabel(ylabel)
        ax.grid(True, alpha=0.25)
        ax.legend()
        fig.tight_layout()
        fig.savefig(FIG / filename, dpi=160)
        plt.close(fig)
    print(f"Base piloto validada: {len(df)} linhas (proveniência secundária pendente de SIDRA).")
    print(f"Indicadores: {OUT / 'indicadores_piloto.csv'}")
    print(f"Auditoria: {OUT / 'auditoria_base_piloto.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
