import datetime
import re
from dataclasses import asdict

from when.logger import logger
from when.rules import F, Match, Options, Rule, Strategy
from when.rules.context import Context
from when.rules.zh import pattern, utils


def casual_year_month(s: Strategy) -> Rule:
    format = "%Y-%m"
    regexp = re.compile("|".join([pattern.COMMON_YEAR_MONTH_PATTERN, pattern.CASUAL_YEAR_MONTH_PATTERN]))
    return F(format=format, regexp=regexp, applier=casual_year_month_applier)


def casual_year_month_applier(m: Match, ctx: Context, op: Options, base: datetime.datetime) -> bool:
    logger.debug(f"casual_year_month matched: {asdict(m)}")

    if len(m.captures) % 2 != 0:
        logger.debug("invalid captures length")
        return False

    ctx.hour = 0
    ctx.minute = 0
    ctx.second = 0

    for i in range(0, len(m.captures), 2):
        year = m.captures[i]
        month = m.captures[i + 1]
        if year == "" or year is None or month == "" or month is None:
            continue

        ctx.year = base.year
        dt, ok = utils.parse_year_from_casual_year(year, base)
        if ok:
            ctx.year = dt.year
            ctx.month = dt.month
            ctx.day = dt.day

        dt, ok = utils.parse_month_from_casual_month(month, base)
        if ok:
            ctx.month = dt.month
            ctx.day = dt.day

    return True


def casual_month(s: Strategy) -> Rule:
    format = "%Y-%m"
    regexp = re.compile("|".join([pattern.CASUAL_MONTH_PATTERN]))
    return F(format=format, regexp=regexp, applier=casual_month_applier)


def casual_month_applier(m: Match, ctx: Context, op: Options, base: datetime.datetime) -> bool:
    logger.debug(f"casual_month matched: {asdict(m)}")

    ctx.hour = 0
    ctx.minute = 0
    ctx.second = 0

    for item in m.captures:
        month = item
        if month == "" or month is None:
            continue

        ctx.year = base.year
        dt, ok = utils.parse_month_from_casual_month(month, base)
        if ok:
            ctx.month = dt.month
            ctx.day = dt.day

    return True
