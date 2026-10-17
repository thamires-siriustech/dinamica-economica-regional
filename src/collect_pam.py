"""Coleta e padroniza a PAM (tabela 1612) do IBGE/SIDRA.

Execute na raiz do projeto: python src/collect_pam.py
A resposta original é preservada em data/raw e a versão normalizada é gravada
em data/processed/pam_municipal_tratada.csv.
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "municipios.csv"
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
BASE_URL = "https://apisidra.ibge.gov.br/values"
TABLE_ID = "1612"
YEARS = list(range(2015, 2026))
TIMEOUT_SECONDS = 60


def _simplify(text: Any) -> str:
    value = unicodedata.normalize("NFKD", str(text)).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", value).strip().casefold()


def _find_header_key(headers: dict[str, str], keyword: str, code: bool = False) -> str | None:
    target = _simplify(keyword)
    for key, label in headers.items():
        normalized = _simplify(label)
        if target in normalized and ("codigo" in normalized) == code:
            return key
    return None


def normalize_sidra_payload(payload: list[dict[str, Any]], municipalities: pd.DataFrame) -> pd.DataFrame:
    """Converte resposta SIDRA em formato longo, preservando marcadores originais."""
    if not isinstance(payload, list) or len(payload) < 2 or not isinstance(payload[0], dict):
        raise ValueError("Resposta SIDRA vazia ou em formato inesperado.")
    headers = {str(k): str(v) for k, v in payload[0].items()}
    if not any(_simplify(v) == "valor" for v in headers.values()):
        raise ValueError("Não foi localizada a linha de descritores da API SIDRA.")

    municipality_name_key = _find_header_key(headers, "municipio", code=False)
    municipality_code_key = _find_header_key(headers, "municipio", code=True)
    year_name_key = _find_header_key(headers, "ano", code=False)
    year_code_key = _find_header_key(headers, "ano", code=True)
    variable_name_key = _find_header_key(headers, "variavel", code=False)
    variable_code_key = _find_header_key(headers, "variavel", code=True)
    product_name_key = _find_header_key(headers, "produto", code=False)
    product_code_key = _find_header_key(headers, "produto", code=True)
    unit_name_key = _find_header_key(headers, "unidade de medida", code=False)
    unit_code_key = _find_header_key(headers, "unidade de medida", code=True)
    value_key = next((k for k, v in headers.items() if _simplify(v) == "valor"), None)

    required = {
        "código do município": municipality_code_key,
        "município": municipality_name_key,
        "ano": year_name_key or year_code_key,
        "variável": variable_name_key,
        "produto": product_name_key,
        "valor": value_key,
    }
    missing = [name for name, key in required.items() if key is None]
    if missing:
        raise ValueError("Não foi possível identificar colunas SIDRA: " + ", ".join(missing))

    frame = pd.DataFrame(payload[1:])
    frame = frame.rename(columns={
        municipality_code_key: "codigo_ibge",
        municipality_name_key: "municipio_fonte",
        (year_name_key or year_code_key): "ano_fonte",
        variable_name_key: "variavel",
        product_name_key: "produto",
        value_key: "valor_sidra_original",
    })
    if variable_code_key:
        frame = frame.rename(columns={variable_code_key: "codigo_variavel"})
    if product_code_key:
        frame = frame.rename(columns={product_code_key: "codigo_produto"})
    if unit_name_key:
        frame = frame.rename(columns={unit_name_key: "unidade"})
    if unit_code_key:
        frame = frame.rename(columns={unit_code_key: "codigo_unidade"})

    frame["codigo_ibge"] = frame["codigo_ibge"].astype(str).str.zfill(7)
    mun = municipalities.copy()
    mun["codigo_ibge"] = mun["codigo_ibge"].astype(str).str.zfill(7)
    known = set(mun["codigo_ibge"])
    returned = set(frame["codigo_ibge"].dropna())
    unexpected = sorted(returned - known)
    if unexpected:
        raise ValueError(f"A API retornou municípios fora da configuração: {unexpected}")
    name_map = mun.set_index("codigo_ibge")["municipio"].to_dict()
    frame["municipio"] = frame["codigo_ibge"].map(name_map)
    frame["ano"] = pd.to_numeric(frame["ano_fonte"], errors="coerce").astype("Int64")
    raw_value = frame["valor_sidra_original"].astype(str).str.strip()
    frame["valor_sidra_original"] = raw_value
    frame["status_valor"] = "numérico"
    frame.loc[raw_value.eq("-"), "status_valor"] = "zero absoluto (marcador SIDRA)"
    frame.loc[raw_value.eq(".."), "status_valor"] = "não se aplica"
    frame.loc[raw_value.eq("..."), "status_valor"] = "não disponível"
    frame.loc[raw_value.str.casefold().eq("x"), "status_valor"] = "valor inibido"
    letters = raw_value.str.fullmatch(r"[A-WY-Z]", case=False, na=False)
    frame.loc[letters, "status_valor"] = "faixa de precisão (marcador SIDRA)"
    numeric = raw_value.where(~raw_value.eq("-"), "0")
    frame["valor"] = pd.to_numeric(numeric, errors="coerce")

    ordered = [
        "codigo_ibge", "municipio", "ano", "produto", "codigo_produto",
        "variavel", "codigo_variavel", "valor", "valor_sidra_original",
        "status_valor", "unidade", "codigo_unidade",
    ]
    for col in ordered:
        if col not in frame.columns:
            frame[col] = pd.NA
    frame = frame[ordered].copy()
    frame = frame.dropna(subset=["codigo_ibge", "ano", "produto", "variavel"])
    frame["ano"] = frame["ano"].astype(int)
    frame = frame.sort_values(["municipio", "ano", "produto", "variavel"]).reset_index(drop=True)

    key = ["codigo_ibge", "ano", "produto", "variavel"]
    duplicated = frame.duplicated(key, keep=False)
    if duplicated.any():
        example = frame.loc[duplicated, key].head(5).to_dict("records")
        raise ValueError(
            f"Chaves duplicadas na granularidade esperada ({int(duplicated.sum())} linhas): {example}"
        )
    return frame


def _session() -> requests.Session:
    session = requests.Session()
    retry = Retry(
        total=3, connect=3, read=2, backoff_factor=1.2,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(["GET"]),
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def main() -> int:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    municipalities = pd.read_csv(CONFIG_PATH, dtype={"codigo_ibge": str})
    codes = ",".join(municipalities["codigo_ibge"].tolist())
    periods = ",".join(map(str, YEARS))
    url = f"{BASE_URL}/t/{TABLE_ID}/n6/{codes}/c81/allxt/p/{periods}/v/allxp"
    print(f"Consultando SIDRA: tabela {TABLE_ID}; períodos {YEARS[0]}–{YEARS[-1]}")
    print(f"Municípios: {', '.join(municipalities['municipio'])}")
    print(f"URL: {url}")

    try:
        response = _session().get(
            url, timeout=TIMEOUT_SECONDS,
            headers={"User-Agent": "portfolio-dinamica-economica-regional/0.6"},
        )
        response.raise_for_status()
        payload = response.json()
    except (requests.RequestException, json.JSONDecodeError) as exc:
        print(f"Falha ao consultar a API SIDRA: {exc}", file=sys.stderr)
        print("Nenhum resultado foi presumido. Verifique a conexão e execute novamente.", file=sys.stderr)
        return 1

    if not isinstance(payload, list) or not payload:
        print("A API não retornou uma lista de dados. Nenhum CSV foi gerado.", file=sys.stderr)
        return 1

    collected_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = RAW_DIR / f"pam_1612_sidra_{timestamp}.json"
    csv_path = RAW_DIR / f"pam_1612_sidra_{timestamp}.csv"
    metadata_path = RAW_DIR / f"pam_1612_metadata_{timestamp}.json"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    pd.DataFrame(payload).to_csv(csv_path, index=False, encoding="utf-8-sig")

    try:
        normalized = normalize_sidra_payload(payload, municipalities)
    except (ValueError, KeyError, TypeError) as exc:
        metadata = {
            "source": "IBGE/SIDRA — Produção Agrícola Municipal (PAM)",
            "table_id": TABLE_ID,
            "table_url": "https://sidra.ibge.gov.br/tabela/1612",
            "api_url": url,
            "municipalities": municipalities.to_dict(orient="records"),
            "requested_years": YEARS,
            "collected_at_utc": collected_at,
            "normalization_error": str(exc),
            "raw_json": str(json_path.relative_to(ROOT)),
            "raw_csv": str(csv_path.relative_to(ROOT)),
        }
        metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Resposta bruta preservada, mas normalização precisa de revisão: {exc}", file=sys.stderr)
        return 2

    processed_path = PROCESSED_DIR / "pam_municipal_tratada.csv"
    normalized.to_csv(processed_path, index=False, encoding="utf-8-sig")
    metadata = {
        "source": "IBGE/SIDRA — Produção Agrícola Municipal (PAM)",
        "table_id": TABLE_ID,
        "table_url": "https://sidra.ibge.gov.br/tabela/1612",
        "api_url": url,
        "municipalities": municipalities.to_dict(orient="records"),
        "requested_years": YEARS,
        "collected_at_utc": collected_at,
        "raw_json": str(json_path.relative_to(ROOT)),
        "raw_csv": str(csv_path.relative_to(ROOT)),
        "processed_csv": str(processed_path.relative_to(ROOT)),
        "raw_record_count_including_descriptor_row": len(payload),
        "processed_record_count": int(len(normalized)),
        "years_returned": sorted(int(year) for year in normalized["ano"].unique()),
        "municipalities_returned": sorted(normalized["municipio"].dropna().unique().tolist()),
        "notes": [
            "A ausência de município/ano/produto não deve ser interpretada como zero.",
            "O marcador SIDRA '-' foi interpretado como zero absoluto; outros marcadores foram preservados.",
            "Valores monetários são nominais, salvo aplicação explícita de deflator.",
            "A granularidade foi validada por município × ano × produto × variável.",
        ],
    }
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Extração bruta: {json_path.relative_to(ROOT)}")
    print(f"Base tratada: {processed_path.relative_to(ROOT)}")
    print(f"Registros tratados: {len(normalized):,}")
    print(f"Anos retornados: {metadata['years_returned']}")
    print(f"Municípios retornados: {', '.join(metadata['municipalities_returned'])}")
    print("Próximo passo: abrir notebooks/01_exploracao_pam.ipynb e validar cobertura e unidades.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
