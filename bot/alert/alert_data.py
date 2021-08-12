from dataclasses import dataclass
from datetime import datetime, timedelta
from math import ceil

from bot.common.user_custom import UserCustom


@dataclass
class AlertData:
    id_: int
    created_by: UserCustom
    repeat_interval: timedelta  # Interval in days
    event_name: str
    next_time: datetime

    def __lt__(self, other):
        if isinstance(other, AlertData):
            return self.next_time < other.next_time
        return NotImplemented

    def alert_text(self):
        return f'"{self.event_name}" starts at {self.next_time}' \
               + ('' if not self.expired else ' (FINAL OCCURRENCE)')

    def advance_alert_time(self):
        if not self.expired:
            self.next_time += self.repeat_interval
            if self.next_time < datetime.now():
                diff = datetime.now() - self.next_time
                multiple = ceil(
                    diff.total_seconds() /
                    self.repeat_interval.total_seconds())
                temp = self.repeat_interval * multiple
                self.next_time += temp
                assert self.next_time > datetime.now()
        # TODO: Ensure time is now in the future

    @property
    def expired(self):
        return self.repeat_interval.total_seconds() == 0

    def __str__(self):
        return f'ID: {self.id_}, "{self.event_name}" every ' \
               f'{self.repeat_interval.days} days. Next occurs at ' \
               f'{self.next_time}'
