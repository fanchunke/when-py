from typing import List

from when.rules import Rule, Strategy
from when.rules.zh.casual_date import casual_date

all: List[Rule] = [
    casual_date(Strategy.Override),
]
