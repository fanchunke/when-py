import datetime

import pytest

import when
from when.rules import Strategy, UnionF
from when.rules.zh.casual_month_day import casual_day, casual_month_day


@pytest.mark.parametrize(
    'text, expected',
    [
        ("6.5", f"{datetime.datetime.now().year}-06-05"),
        ("6月1号", f"{datetime.datetime.now().year}-06-01"),
        ("上个月2号", f"{datetime.datetime.now().year}-{datetime.datetime.now().month-1:>02}-02"),
        ("5月30", f"{datetime.datetime.now().year}-05-30"),
        ("本月5号", f"{datetime.datetime.now().year}-{datetime.datetime.now().month:>02}-05"),
        ("5/19", f"{datetime.datetime.now().year}-05-19"),
        ("5月31", f"{datetime.datetime.now().year}-05-31"),
        ("5号", f"{datetime.datetime.now().year}-{datetime.datetime.now().month:>02}-05"),
        ("test", ""),
    ],
)
def test_casual_year(text: str, expected: str):
    p = when.new()
    f = UnionF(rules=[casual_month_day(Strategy.Override), casual_day(Strategy.Override)])
    p.add([f])
    result = p.parse(text)
    got = ""
    if result is not None:
        got = result.format()
    assert got == expected, f"test_casual_year() text: {text}, got: {got}, expected: {expected}"
