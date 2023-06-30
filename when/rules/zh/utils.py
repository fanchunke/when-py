import calendar
import datetime
from typing import Tuple

from when.rules.zh import pattern


def add_months(d: datetime.datetime, offset: int) -> datetime.datetime:
    month = d.month - 1 + offset
    year = d.year + month // 12
    month = month % 12 + 1
    day = min(d.day, calendar.monthrange(year, month)[1])
    return datetime.datetime(year, month, day)


def parse_year_from_casual_year(text: str, base: datetime.datetime) -> Tuple[datetime.datetime, bool]:
    chinese_num = "零〇一二三四五六七八九"
    arabic_num = "00123456789"
    replacer = str.maketrans(chinese_num, arabic_num)
    year = text.translate(replacer)

    today = datetime.datetime.now()
    offset = pattern.CASUAL_YEAY_WORD.get(year)
    if year.isdigit():
        if len(year) <= 2:
            return datetime.datetime(year=today.year // 100 * 100 + int(year), month=1, day=1), True
        else:
            return datetime.datetime(year=int(year), month=1, day=1), True
    elif offset is not None:
        return datetime.datetime(year=today.year + offset, month=1, day=1), True
    else:
        return base, False


def parse_month_from_casual_month(text: str, base: datetime.datetime) -> Tuple[datetime.datetime, bool]:
    month_int = pattern.MON_WORDS.get(text)
    offset = pattern.CASUAL_MONTH_WORD.get(text)
    if text.isdigit():
        return datetime.datetime(year=base.year, month=int(text), day=1), True
    elif month_int is not None:
        return datetime.datetime(year=base.year, month=month_int, day=1), True
    elif offset is not None:
        dt = datetime.datetime(year=base.year, month=base.month, day=1)
        dt = add_months(dt, offset)
        return dt, True
    else:
        return base, False


def parse_day_from_casual_day(text: str) -> Tuple[int, bool]:
    day_int = pattern.DAY_WORDS.get(text)
    if text.isdigit():
        return int(text), True
    elif day_int is not None:
        return day_int, True
    else:
        return 0, False
