import os
import unittest
from datetime import datetime

from ofxstatement.statement import Statement
from ofxstatement.ui import UI

from ofxstatement_satispay.plugin import SatispayPlugin


class TestSatispayPlugin(unittest.TestCase):
  def test_satispay(self) -> None:
    plugin = SatispayPlugin(UI(), {})
    here = os.path.dirname(__file__)
    satispay_filename = os.path.join(here, "satispay-statement.csv")

    parser = plugin.get_parser(satispay_filename)
    statement: Statement = parser.parse()

    self.assertIsNotNone(statement)
    self.assertEqual(len(statement.lines), 4)

    self.assertEqual(
      statement.start_date, datetime.fromisoformat("2022-03-01T09:44:27")
    )
    self.assertEqual(statement.end_date, datetime.fromisoformat("2024-07-24T02:59:45"))

    self.assertEqual(statement.lines[3].id, "17f08d62-7e44-4400-b849-6b1f4bb1d546")
    self.assertEqual(statement.lines[2].payee, "Ajeje Brazorf")
    self.assertEqual(statement.lines[1].amount, -2)
    self.assertEqual(statement.lines[0].currency.symbol, "EUR")
    self.assertEqual(statement.lines[3].memo, "kind: BANK")
    self.assertEqual(
      statement.lines[2].memo, "kind: P2P, comment: Adesso lo trovo il biglietto 🎟️"
    )


if __name__ == "__main__":
  unittest.main()
