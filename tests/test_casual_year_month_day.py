import datetime

import pytest

import when
from when.rules import Strategy
from when.rules.zh.casual_year_month_day import casual_year_month_day


@pytest.mark.parametrize(
    'text, expected',
    [
        ("2023-4-10", "2023-04-10"),
        ("2023年3月10", "2023-03-10"),
        ("今年6月5号", f"{datetime.datetime.now().year}-06-05"),
        ("2022/2/1", "2022-02-01"),
        ("去年11月11号", f"{datetime.datetime.now().year-1}-11-11"),
        ("19年11月15日", "2019-11-15"),
        ("今年5月22", f"{datetime.datetime.now().year}-05-22"),
        ("test", ""),
    ],
)
def test_casual_year_month_day(text: str, expected: str):
    p = when.new()
    p.add([casual_year_month_day(Strategy.Override)])
    result = p.parse(text)
    got = ""
    if result is not None:
        got = result.format()
    assert got == expected, f"test_casual_year_month_day() text: {text}, got: {got}, expected: {expected}"
