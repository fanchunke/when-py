import datetime
import re
from dataclasses import asdict

from when.logger import logger
from when.rules import F, Match, Options, Rule, Strategy
from when.rules.context import Context
from when.rules.zh import pattern, utils


def casual_month_day(s: Strategy) -> Rule:
    format = "%Y-%m-%d"
    regexp = re.compile("|".join([pattern.CASUAL_MONTH_DAY_PATTERN]))
    return F(format=format, regexp=regexp, applier=casual_month_day_applier)


def casual_month_day_applier(m: Match, ctx: Context, op: Options, base: datetime.datetime) -> bool:
    logger.debug(f"casual_month_day matched: {asdict(m)}")

    if len(m.captures) % 2 != 0:
        logger.debug("invalid captures length")
        return False

    ctx.hour = 0
    ctx.minute = 0
    ctx.second = 0

    for i in range(0, len(m.captures), 2):
        month = m.captures[i]
        day = m.captures[i + 1]
        if month == "" or month is None or day == "" or day is None:
            continue

        ctx.year = base.year
        dt, ok = utils.parse_month_from_casual_month(month, base)
        if ok:
            ctx.month = dt.month
            ctx.day = dt.day

        day_int, ok = utils.parse_day_from_casual_day(day)
        if ok:
            ctx.day = day_int

    return True


def casual_day(s: Strategy) -> Rule:
    format = "%Y-%m-%d"
    regexp = re.compile("|".join([pattern.CASUAL_DAY_PATTERN]))
    return F(format=format, regexp=regexp, applier=casual_day_applier)


def casual_day_applier(m: Match, ctx: Context, op: Options, base: datetime.datetime) -> bool:
    logger.debug(f"casual_day matched: {asdict(m)}")

    ctx.hour = 0
    ctx.minute = 0
    ctx.second = 0

    for item in m.captures:
        day = item
        if day == "" or day is None:
            continue

        ctx.year = base.year
        ctx.month = base.month
        day_int, ok = utils.parse_day_from_casual_day(day)
        if ok:
            ctx.day = day_int

    return True
