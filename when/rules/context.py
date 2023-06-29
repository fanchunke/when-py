import datetime
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Context(object):
    text: str = field(default="")
    duration: Optional[datetime.timedelta] = field(default=None)
    year: Optional[int] = field(default=None)
    month: Optional[int] = field(default=None)
    weekday: Optional[int] = field(default=None)
    day: Optional[int] = field(default=None)
    hour: Optional[int] = field(default=None)
    minute: Optional[int] = field(default=None)
    second: Optional[int] = field(default=None)
    tzinfo: Optional[datetime.tzinfo] = field(default=None)

    def time(self, t: datetime.datetime) -> datetime.datetime:
        if self.duration is not None:
            t = t + self.duration

        if self.year is not None:
            t = datetime.datetime(
                self.year,
                t.month,
                t.day,
                t.hour,
                t.minute,
                t.second,
                t.microsecond,
                t.tzinfo,
            )

        if self.month is not None:
            t = datetime.datetime(
                t.year,
                self.month,
                t.day,
                t.hour,
                t.minute,
                t.second,
                t.microsecond,
                t.tzinfo,
            )

        if self.day is not None:
            t = datetime.datetime(
                t.year,
                t.month,
                self.day,
                t.hour,
                t.minute,
                t.second,
                t.microsecond,
                t.tzinfo,
            )

        if self.hour is not None:
            t = datetime.datetime(
                t.year,
                t.month,
                t.day,
                self.hour,
                t.minute,
                t.second,
                t.microsecond,
                t.tzinfo,
            )

        if self.minute is not None:
            t = datetime.datetime(
                t.year,
                t.month,
                t.day,
                t.hour,
                self.minute,
                t.second,
                t.microsecond,
                t.tzinfo,
            )

        if self.second is not None:
            t = datetime.datetime(
                t.year,
                t.month,
                t.day,
                t.hour,
                t.minute,
                self.second,
                t.microsecond,
                t.tzinfo,
            )

        if self.tzinfo is not None:
            t = datetime.datetime(
                t.year,
                t.month,
                t.day,
                t.hour,
                t.minute,
                t.second,
                t.microsecond,
                self.tzinfo,
            )

        return t
