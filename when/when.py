import datetime
from dataclasses import dataclass, field
from typing import Callable, List, Optional

from when.rules import Context, Match, Options, Rule


@dataclass
class Result(object):
    index: int = field(default=0)
    text: str = field(default="")
    source: str = field(default="")
    time: datetime.datetime = field(default_factory=datetime.datetime.now)
    _format: str = field(default="%Y-%m-%d %H:%M:%S")

    def format(self) -> str:
        return self.time.strftime(self._format)


MiddlewareFunc = Callable[[str], str]


@dataclass
class Parser(object):
    options: Optional[Options] = field(default_factory=Options.default)
    rules: List[Rule] = field(default_factory=list)
    middlewares: List[MiddlewareFunc] = field(default_factory=list)

    def parse(self, text: str, base: Optional[datetime.datetime] = None) -> Optional[Result]:
        if base is None:
            base = datetime.datetime.now()

        result = Result(source=text, time=base, index=-1)

        if self.options is None:
            self.options = Options(distance=5, match_by_order=True)

        # apply middleware
        for m in self.middlewares:
            text = m(text)

        # find all matches
        matches: List[Match] = []
        c = 0
        for rule in self.rules:
            r = rule.find(text)
            if r is not None:
                r.order = c
                c += 1
                matches.append(r)

        # not found
        if len(matches) == 0:
            return None

        # sort
        matches = sorted(matches, key=lambda x: x.left)

        # get borders of the matches
        end = matches[0].right
        result.index = matches[0].left
        for i, match in enumerate(matches):
            if match.left <= end + self.options.distance:
                end = match.right
            else:
                matches = matches[:i]
        result.text = text[result.index : end]

        # apply rules
        if self.options.match_by_order:
            matches = sorted(matches, key=lambda x: x.order)

        ctx = Context(text=result.text)
        applied = False
        for applier in matches:
            ok = applier.apply(ctx, self.options, result.time)
            applied = ok or applied
            result._format = applier.format

        if not applied:
            return None

        ctx_time = ctx.time(result.time)
        if ctx_time is None:
            return None
        result.time = ctx_time
        return result

    def add(self, r: List[Rule]) -> None:
        self.rules.extend(r)

    def use(self, f: MiddlewareFunc) -> None:
        self.middlewares.append(f)

    def set_options(self, op: Options) -> None:
        self.options = op
