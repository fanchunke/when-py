import abc
import datetime
import enum
import re
from dataclasses import dataclass, field
from typing import Callable, List, Optional

from when.rules.context import Context


class Strategy(enum.IntEnum):
    Skip = 0
    Merge = 1
    Override = 2


@dataclass
class Options(object):
    afternoon: int = field(default=0)
    evening: int = field(default=0)
    morning: int = field(default=0)
    noon: int = field(default=0)
    distance: int = field(default=0)
    match_by_order: bool = field(default=False)


ApplierFunc = Callable[["Match", Context, Options, datetime.datetime], bool]


@dataclass
class Match(object):
    applier: ApplierFunc
    left: int = field(default=0)
    right: int = field(default=0)
    text: str = field(default="")
    captures: List[str] = field(default_factory=list)
    order: int = field(default=0)
    format: str = field(default="")

    def apply(self, ctx: Context, op: Options, t: datetime.datetime) -> bool:
        return self.applier(self, ctx, op, t)


class Rule(abc.ABC):
    def find(self, text: str) -> Optional[Match]:
        raise NotImplementedError


@dataclass
class F(Rule):
    regexp: re.Pattern
    applier: ApplierFunc
    format: str

    def find(self, text: str) -> Optional[Match]:
        matched = self.regexp.search(text)
        if not matched:
            return None

        left = matched.start()
        right = matched.end()
        captures = list(matched.groups())
        m = Match(
            applier=self.applier,
            left=left,
            right=right,
            captures=captures,
            format=self.format,
        )

        return m


@dataclass
class UnionF(Rule):
    rules: List[Rule]

    def add_rule(self, rs: List[Rule]) -> None:
        self.rules.extend(rs)

    def find(self, text: str) -> Optional[Match]:
        matches: List[Match] = []
        c = 0
        for r in self.rules:
            m = r.find(text)
            if m is not None:
                m.order = c
                c += 1
                matches.append(m)

        if len(matches) == 0:
            return None

        matches = sorted(matches, key=lambda x: len(x.text), reverse=True)
        return matches[0]
