import datetime
from typing import Tuple

from when.rules.zh import pattern


def parse_year_from_casual_year(text: str) -> Tuple[int, bool]:
    chinese_num = "零〇一二三四五六七八九"
    arabic_num = "00123456789"
    replacer = str.maketrans(chinese_num, arabic_num)
    year = text.translate(replacer)

    today = datetime.datetime.now()
    offset = pattern.CASUAL_YEAY_WORD.get(year)
    if year.isdigit():
        if len(year) <= 2:
            return today.year // 100 * 100 + int(year), True
        else:
            return int(year), True
    elif offset is not None:
        return (today + datetime.timedelta(days=offset)).year, True
    else:
        return 0, False
