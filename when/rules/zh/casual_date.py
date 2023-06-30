from typing import List

from when.rules import Rule, Strategy, UnionF
from when.rules.zh.casual_month_day import casual_day, casual_month_day
from when.rules.zh.casual_year import casual_year
from when.rules.zh.casual_year_month import casual_month, casual_year_month
from when.rules.zh.casual_year_month_day import casual_year_month_day


def casual_date(s: Strategy) -> Rule:
    rules: List[Rule] = [
        casual_year_month_day(s),
        casual_year_month(s),
        casual_year(s),
        casual_month_day(s),
        casual_month(s),
        casual_day(s),
    ]
    f = UnionF(rules=rules)
    return f
