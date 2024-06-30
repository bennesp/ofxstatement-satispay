import unittest
from datetime import datetime

from ofxstatement_satispay.utils import parse_it_datetime

class TestUtils(unittest.TestCase):
  def test_parse_it_datetime(self) -> None:
    d1 = "1 mar 2022. 09:44:27"
    d2 = "24 lug 2024. 02:59:45"
    d3 = "12 dic 2023. 23:59:59"

    self.assertEqual(parse_it_datetime(d1), datetime.fromisoformat("2022-03-01T09:44:27"))
    self.assertEqual(parse_it_datetime(d2), datetime.fromisoformat("2024-07-24T02:59:45"))
    self.assertEqual(parse_it_datetime(d3), datetime.fromisoformat("2023-12-12T23:59:59"))
