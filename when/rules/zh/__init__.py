from typing import List

from when.rules import Rule, Strategy
from when.rules.zh.casual_year import casual_year

all: List[Rule] = [
    casual_year(Strategy.Override),
]
