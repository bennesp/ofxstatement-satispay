import re
from datetime import datetime
from decimal import Decimal

months = {
  "gen": 1,
  "feb": 2,
  "mar": 3,
  "apr": 4,
  "mag": 5,
  "giu": 6,
  "lug": 7,
  "ago": 8,
  "set": 9,
  "ott": 10,
  "nov": 11,
  "dic": 12,
}


def parse_it_datetime(date: str) -> datetime:
  # Parse a date in the format "1 mar 2022. 09:44:27" to a datetime object
  r = re.compile(r"^(\d{1,2})\s(\w{3})\s(\d{4})\.\s(\d{2}:\d{2}:\d{2})$")
  m = r.match(date)
  if not m:
    raise ValueError(f"Date {date} does not match the expected format")
  day, month, year, time = m.groups()
  month = months[month]

  return datetime(
    int(year), month, int(day), int(time[:2]), int(time[3:5]), int(time[6:8])
  )


def parse_it_decimal(amount: str) -> Decimal:
  # Parse an amount in the format "1.234,56" to a Decimal object
  try:
    return Decimal(amount.replace(".", "").replace(",", "."))
  except Exception as e:
    raise ValueError(f"Amount {amount} does not match the expected format: {e}")
