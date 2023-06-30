import datetime

import pytest

import when
from when.rules import Strategy
from when.rules.zh.casual_year import casual_year


@pytest.mark.parametrize(
    'text, expected',
    [
        ("2022年", "2022"),
        ("二零二三年", "2023"),
        ("去年", str(datetime.datetime.now().year - 1)),
        ("今年", str(datetime.datetime.now().year)),
        ("明年", str(datetime.datetime.now().year + 1)),
        ("test", ""),
    ],
)
def test_casual_year(text: str, expected: str):
    p = when.new()
    p.add([casual_year(Strategy.Override)])
    result = p.parse(text)
    got = ""
    if result is not None:
        got = result.format()
    assert got == expected, f"test_casual_year() text: {text}, got: {got}, expected: {expected}"
