"""Reproduz análise exploratória do piloto de emprego de 2025.

Entrada é uma transcrição secundária documentada, não microdados oficiais reconciliados.
"""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"
OUT = ROOT / "reports" / "outputs"
FIG = ROOT / "reports" / "figures"

def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    summary = pd.read_csv(DATA / "caged_resumo_municipal_2025_secundario.csv", dtype={"codigo_ibge": str})
    sector = pd.read_csv(DATA / "caged_setor_2025_secundario.csv", dtype={"codigo_ibge": str})
    if not (summary.admissoes - summary.desligamentos == summary.saldo).all():
        raise ValueError("Saldo municipal divergente de admissões menos desligamentos.")
    for _, row in summary.iterrows():
        sub = sector[sector.municipio.eq(row.municipio)]
        for col in ("admissoes", "desligamentos", "saldo"):
            if int(sub[col].sum()) != int(row[col]):
                raise ValueError(f"Soma setorial de {col} não confere para {row.municipio}.")
    fig, ax = plt.subplots(figsize=(9, 5))
    ordered = summary.sort_values("saldo")
    ax.barh(ordered.municipio, ordered.saldo)
    ax.axvline(0, color="black", linewidth=0.7)
    ax.set_title("Saldo de empregos formais — 2025 (piloto secundário)")
    ax.set_xlabel("Admissões − desligamentos")
    fig.tight_layout()
    fig.savefig(FIG / "saldo_emprego_municipios_2025_piloto.png", dpi=180)
    plt.close(fig)
    sector.groupby(["municipio", "setor_agregado"], as_index=False).agg(
        admissoes=("admissoes","sum"), desligamentos=("desligamentos","sum"), saldo=("saldo","sum")
    ).to_csv(OUT / "indicadores_emprego_setor_2025.csv", index=False, encoding="utf-8-sig")
    print(f"Municípios: {len(summary)}; linhas setoriais: {len(sector)}")
    print("Aviso: dados secundários, pendentes de conciliação com microdados oficiais do MTE.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
