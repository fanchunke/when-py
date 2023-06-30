import datetime

import pytest

import when
from when.rules import Strategy, UnionF
from when.rules.zh.casual_year_month import casual_month, casual_year_month


@pytest.mark.parametrize(
    'text, expected',
    [
        ("4月份", f"{datetime.datetime.now().year}-04"),
        ("4月", f"{datetime.datetime.now().year}-04"),
        ("本月", datetime.datetime.now().strftime("%Y-%m")),
        ("2022年3月", "2022-03"),
        ("去年7月", f"{datetime.datetime.now().year-1}-07"),
        ("2023-4", "2023-04"),
        ("今年3月", f"{datetime.datetime.now().year}-03"),
        ("今年2月", f"{datetime.datetime.now().year}-02"),
        ("前年9月", f"{datetime.datetime.now().year-2}-09"),
        ("2023/4", "2023-04"),
        ("test", ""),
    ],
)
def test_casual_year_month(text: str, expected: str):
    p = when.new()
    f = UnionF(rules=[casual_year_month(Strategy.Override), casual_month(Strategy.Override)])
    p.add([f])
    result = p.parse(text)
    got = ""
    if result is not None:
        got = result.format()
    assert got == expected, f"test_casual_year_month() text: {text}, got: {got}, expected: {expected}"
