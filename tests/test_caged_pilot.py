"""Valida consistência interna dos dados secundários do piloto, não a fonte oficial."""
import unittest
from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]

class TestCagedPilot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.summary = pd.read_csv(ROOT / "data/processed/caged_resumo_municipal_2025_secundario.csv", dtype={"codigo_ibge":str})
        cls.sector = pd.read_csv(ROOT / "data/processed/caged_setor_2025_secundario.csv", dtype={"codigo_ibge":str})
        cls.audit = pd.read_csv(ROOT / "data/processed/auditoria_fontes_saldo_lucas_2025.csv", dtype={"codigo_ibge":str})

    def test_expected_municipalities(self):
        self.assertEqual(set(self.summary.municipio), {"Lucas do Rio Verde","Sorriso","Nova Mutum"})
        self.assertEqual(len(self.summary), 3)

    def test_balance_arithmetic(self):
        self.assertTrue((self.summary.admissoes - self.summary.desligamentos == self.summary.saldo).all())

    def test_sector_totals_match_municipal_summary(self):
        for _, row in self.summary.iterrows():
            sub = self.sector[self.sector.municipio.eq(row.municipio)]
            self.assertEqual(int(sub.admissoes.sum()), int(row.admissoes))
            self.assertEqual(int(sub.desligamentos.sum()), int(row.desligamentos))
            self.assertEqual(int(sub.saldo.sum()), int(row.saldo))

    def test_discrepancy_is_preserved(self):
        self.assertEqual(set(self.audit.saldo_empregos), {1767,1803})

    def test_status_marks_secondary_source(self):
        self.assertTrue(self.summary.status.str.contains("secundario").all())

if __name__ == "__main__":
    unittest.main()
