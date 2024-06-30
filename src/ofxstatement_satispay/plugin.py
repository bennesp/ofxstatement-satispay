import csv
from typing import Iterable, List, Optional, IO

from ofxstatement.plugin import Plugin
from ofxstatement.parser import CsvStatementParser
from ofxstatement.statement import Statement, StatementLine, Currency
from ofxstatement.exceptions import ParseError

from .utils import parse_it_datetime, parse_it_decimal


class SatispayPlugin(Plugin):
  """A plugin to parse CSV files exported from Satispay"""

  def get_parser(self, filename: str) -> "SatispayParser":
    fd = open(filename, "r")
    return SatispayParser(fd)


class SatispayParser(CsvStatementParser):
  def __init__(self, fd: IO) -> None:
    super().__init__(fd)
    self.fd = fd

  def parse(self) -> Statement:
    """Main entry point for parsers

    super() implementation will call to split_records and parse_record to
    process the file.
    """
    stmt: Statement = super().parse()
    self.fd.close()

    stmt.bank_id = "Satispay"
    if stmt.lines:
      stmt.start_date = min(stmt.lines, key=lambda x: x.date).date
      stmt.end_date = max(stmt.lines, key=lambda x: x.date).date

    return stmt

  def split_records(self) -> Iterable[str]:
    """Return iterable object consisting of a line per transaction"""
    return csv.DictReader(self.fd, delimiter=",", quotechar='"')

  def parse_record(self, line: List[Optional[str]]) -> StatementLine:
    """Parse given transaction line and return StatementLine object"""
    stmt_line: Optional[StatementLine] = None

    try:
      stmt_line = self.parse_transaction(line)
    except Exception as e:
      raise ParseError(self.cur_record, str(e))

    return stmt_line

  def parse_transaction(self, line: List[Optional[str]]) -> StatementLine:
    """Parse transaction line and return StatementLine object"""
    stmt_line: StatementLine = super().parse_record(line)

    if line["state"] != "APPROVED":
      return None

    stmt_line.id = line["id"]
    stmt_line.payee = line["name"]
    stmt_line.date = parse_it_datetime(line["date"])
    stmt_line.amount = parse_it_decimal(line["amount"])
    stmt_line.currency = Currency(line["currency"])
    stmt_line.memo = f"kind: {line['kind']}"
    if line["extra info"]:
      stmt_line.memo += f", comment: {line['extra info']}"

    return stmt_line
