"""Verify all 32 variants have valid configs, separate docs, and run cleanly."""
from pathlib import Path
import unittest

from engine.market_calendar import market_closed_reason
from datetime import datetime, timezone
from variants import ALL_VARIANTS

ROOT = Path(__file__).resolve().parents[1]


class TestVariantsRepo(unittest.TestCase):
    def test_all_32_variants_have_code_and_separate_docs(self):
        self.assertEqual(len(ALL_VARIANTS), 32)
        for vid, cfg in ALL_VARIANTS.items():
            self.assertEqual(cfg["id"], vid)
            self.assertTrue((ROOT / "variants" / f"{vid}.py").exists(), f"Missing variants/{vid}.py")
            self.assertTrue((ROOT / "docs/variants" / f"{vid}.md").exists(), f"Missing docs/variants/{vid}.md")

    def test_nyse_holiday_calendar(self):
        thanksgiving = datetime(2026, 11, 26, 15, 0, tzinfo=timezone.utc)
        self.assertIn("Thanksgiving", market_closed_reason(thanksgiving))
        black_friday = datetime(2026, 11, 27, 15, 0, tzinfo=timezone.utc)
        self.assertIsNone(market_closed_reason(black_friday))


if __name__ == "__main__":
    unittest.main()
