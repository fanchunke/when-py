import datetime

import pytest

import when
from when.rules import Strategy
from when.rules.zh.casual_date import casual_date


@pytest.mark.parametrize(
    'text, expected',
    [
        ("2022年", "2022"),
        ("二零二三年", "2023"),
        ("去年", str(datetime.datetime.now().year - 1)),
        ("今年", str(datetime.datetime.now().year)),
        ("明年", str(datetime.datetime.now().year + 1)),
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
        ("2023-4-10", "2023-04-10"),
        ("2023年3月10", "2023-03-10"),
        ("今年6月5号", f"{datetime.datetime.now().year}-06-05"),
        ("2022/2/1", "2022-02-01"),
        ("去年11月11号", f"{datetime.datetime.now().year-1}-11-11"),
        ("19年11月15日", "2019-11-15"),
        ("今年5月22", f"{datetime.datetime.now().year}-05-22"),
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
def test_casual_date(text: str, expected: str):
    p = when.new()
    p.add([casual_date(Strategy.Override)])
    result = p.parse(text)
    got = ""
    if result is not None:
        got = result.format()
    assert got == expected, f"test_casual_date() text: {text}, got: {got}, expected: {expected}"
