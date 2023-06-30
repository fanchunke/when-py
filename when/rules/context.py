import datetime
from dataclasses import asdict, dataclass, field
from typing import Optional

from when.logger import logger


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

    def time(self, t: datetime.datetime) -> Optional[datetime.datetime]:
        if self.duration is not None:
            t = t + self.duration

        if self.year is None:
            self.year = t.year

        if self.month is None:
            self.month = t.month

        if self.day is None:
            self.day = t.day

        if self.weekday is not None:
            diff = self.weekday - t.weekday()
            self.day = self.day + diff

        if self.hour is None:
            self.hour = t.hour

        if self.minute is None:
            self.minute = t.minute

        if self.second is None:
            self.second = t.second

        if self.tzinfo is None:
            self.tzinfo = t.tzinfo

        try:
            result = datetime.datetime(
                year=self.year,
                month=self.month,
                day=self.day,
                hour=self.hour,
                minute=self.minute,
                second=self.second,
                microsecond=t.microsecond,
                tzinfo=self.tzinfo,
            )
        except Exception as e:
            logger.warning(f"parse time failed. context: {asdict(self)}, error: {e}")
            return None
        else:
            return result
