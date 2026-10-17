"""Testes unitários offline para a normalização SIDRA."""
import sys
import unittest
from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from collect_pam import normalize_sidra_payload

class NormalizeSidraPayloadTests(unittest.TestCase):
    def setUp(self):
        self.municipalities = pd.DataFrame([
            {"codigo_ibge":"5105259","municipio":"Lucas do Rio Verde","uf":"MT","papel":"principal"},
            {"codigo_ibge":"5107925","municipio":"Sorriso","uf":"MT","papel":"comparacao"},
            {"codigo_ibge":"5106224","municipio":"Nova Mutum","uf":"MT","papel":"comparacao"},
        ])
        self.payload = [
            {"NC":"Nível Territorial (Código)","NN":"Nível Territorial","MC":"Unidade de Medida (Código)","MN":"Unidade de Medida","V":"Valor","D1C":"Município (Código)","D1N":"Município","D2C":"Ano (Código)","D2N":"Ano","D3C":"Variável (Código)","D3N":"Variável","D4C":"Produto das lavouras temporárias (Código)","D4N":"Produto das lavouras temporárias"},
            {"NC":"6","NN":"Município","MC":"t","MN":"Toneladas","V":"1250000","D1C":"5105259","D1N":"Lucas do Rio Verde","D2C":"2024","D2N":"2024","D3C":"214","D3N":"Quantidade produzida","D4C":"2713","D4N":"Soja (em grão)"},
            {"NC":"6","NN":"Município","MC":"t","MN":"Toneladas","V":"-","D1C":"5107925","D1N":"Sorriso","D2C":"2024","D2N":"2024","D3C":"214","D3N":"Quantidade produzida","D4C":"2713","D4N":"Soja (em grão)"},
            {"NC":"6","NN":"Município","MC":"t","MN":"Toneladas","V":"...","D1C":"5106224","D1N":"Nova Mutum","D2C":"2024","D2N":"2024","D3C":"214","D3N":"Quantidade produzida","D4C":"2713","D4N":"Soja (em grão)"},
        ]

    def test_preserves_special_values(self):
        df = normalize_sidra_payload(self.payload, self.municipalities)
        self.assertEqual(len(df), 3)
        self.assertEqual(df.loc[df.municipio.eq("Lucas do Rio Verde"), "valor"].iloc[0], 1250000)
        sorriso = df.loc[df.municipio.eq("Sorriso")].iloc[0]
        self.assertEqual(sorriso["valor"], 0)
        self.assertEqual(sorriso["status_valor"], "zero absoluto (marcador SIDRA)")
        nova = df.loc[df.municipio.eq("Nova Mutum")].iloc[0]
        self.assertTrue(pd.isna(nova["valor"]))
        self.assertEqual(nova["status_valor"], "não disponível")

    def test_rejects_duplicate_keys(self):
        with self.assertRaisesRegex(ValueError, "(?i)chaves duplicadas"):
            normalize_sidra_payload(self.payload + [self.payload[1]], self.municipalities)

    def test_rejects_unconfigured_municipality(self):
        payload = [self.payload[0], {**self.payload[1], "D1C":"9999999"}]
        with self.assertRaisesRegex(ValueError, "fora da configuração"):
            normalize_sidra_payload(payload, self.municipalities)

    def test_inhibited_value_is_not_zero(self):
        payload = [self.payload[0], {**self.payload[1], "V":"x"}]
        df = normalize_sidra_payload(payload, self.municipalities)
        self.assertTrue(pd.isna(df.iloc[0]["valor"]))
        self.assertEqual(df.iloc[0]["status_valor"], "valor inibido")

if __name__ == "__main__":
    unittest.main()
