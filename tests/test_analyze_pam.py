"""Testes offline das regras analíticas; os números são sintéticos."""
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from analyze_pam import build_core_crops, build_coverage_report, build_yoy_table, latest_common_year

class AnalyzePamTests(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame([
            {"codigo_ibge":"5105259","municipio":"Lucas do Rio Verde","ano":2022,"produto":"Soja (em grão)","variavel":"Quantidade produzida","valor":100.0,"unidade":"Toneladas","status_valor":"numérico","valor_sidra_original":"100","produto_norm":"soja (em grao)","variavel_norm":"quantidade produzida"},
            {"codigo_ibge":"5105259","municipio":"Lucas do Rio Verde","ano":2023,"produto":"Soja (em grão)","variavel":"Quantidade produzida","valor":150.0,"unidade":"Toneladas","status_valor":"numérico","valor_sidra_original":"150","produto_norm":"soja (em grao)","variavel_norm":"quantidade produzida"},
            {"codigo_ibge":"5107925","municipio":"Sorriso","ano":2022,"produto":"Soja (em grão)","variavel":"Quantidade produzida","valor":200.0,"unidade":"Toneladas","status_valor":"numérico","valor_sidra_original":"200","produto_norm":"soja (em grao)","variavel_norm":"quantidade produzida"},
            {"codigo_ibge":"5107925","municipio":"Sorriso","ano":2023,"produto":"Soja (em grão)","variavel":"Quantidade produzida","valor":250.0,"unidade":"Toneladas","status_valor":"numérico","valor_sidra_original":"250","produto_norm":"soja (em grao)","variavel_norm":"quantidade produzida"},
        ])

    def test_yoy_for_consecutive_years(self):
        current = build_yoy_table(self.df).query("municipio == 'Lucas do Rio Verde' and ano == 2023").iloc[0]
        self.assertEqual(current["valor_ano_anterior"], 100.0)
        self.assertAlmostEqual(float(current["variacao_percentual"]), 50.0)

    def test_latest_common_year_requires_all_cities(self):
        result = latest_common_year(self.df, "Quantidade produzida", product_pattern=r"soja", municipalities=["Lucas do Rio Verde","Sorriso","Nova Mutum"])
        self.assertIsNone(result)

    def test_coverage_includes_missing_expected_city(self):
        with TemporaryDirectory() as td:
            config = Path(td) / "municipios.csv"
            pd.DataFrame([
                {"codigo_ibge":"5105259","municipio":"Lucas do Rio Verde","papel":"principal"},
                {"codigo_ibge":"5107925","municipio":"Sorriso","papel":"comparacao"},
                {"codigo_ibge":"5106224","municipio":"Nova Mutum","papel":"comparacao"},
            ]).to_csv(config, index=False)
            with patch("analyze_pam.CONFIG_PATH", config):
                coverage = build_coverage_report(self.df)
        missing = coverage.loc[coverage.municipio.eq("Nova Mutum")].iloc[0]
        self.assertFalse(bool(missing["presente_na_extracao"]))
        self.assertEqual(int(missing["linhas"]), 0)

    def test_milho_verde_excluded_from_grain_analysis(self):
        frame = pd.DataFrame([
            {"codigo_ibge":"5105259","municipio":"Lucas do Rio Verde","ano":2025,"produto":"Milho (em grão)","variavel":"Quantidade produzida","valor":10,"valor_sidra_original":"10","status_valor":"numérico","unidade":"Toneladas","produto_norm":"milho (em grao)","variavel_norm":"quantidade produzida"},
            {"codigo_ibge":"5105259","municipio":"Lucas do Rio Verde","ano":2025,"produto":"Milho verde","variavel":"Quantidade produzida","valor":20,"valor_sidra_original":"20","status_valor":"numérico","unidade":"Toneladas","produto_norm":"milho verde","variavel_norm":"quantidade produzida"},
        ])
        self.assertEqual(build_core_crops(frame)["produto"].tolist(), ["Milho (em grão)"])

if __name__ == "__main__":
    unittest.main()
