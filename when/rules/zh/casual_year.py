import datetime
import re
from dataclasses import asdict

from when.logger import logger
from when.rules import F, Match, Options, Rule, Strategy
from when.rules.context import Context
from when.rules.zh import pattern, utils


def casual_year(s: Strategy) -> Rule:
    format = "%Y"
    regexp = re.compile("|".join([pattern.COMMON_YEAR_PATTERN, pattern.CASUAL_YEAR_PATTERN]))
    return F(format=format, regexp=regexp, applier=casual_year_applier)


def casual_year_applier(m: Match, ctx: Context, op: Options, base: datetime.datetime) -> bool:
    logger.debug(f"casual_year matched: {asdict(m)}")
    ctx.hour = 0
    ctx.minute = 0
    ctx.second = 0

    for item in m.captures:
        year = item
        if year == "" or year is None:
            continue

        dt, ok = utils.parse_year_from_casual_year(year, base)
        if ok:
            ctx.year = dt.year
            ctx.month = dt.month
            ctx.day = dt.day

    return True
