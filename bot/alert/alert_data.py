from dataclasses import dataclass
from datetime import datetime

from bot.common.user_custom import UserCustom


@dataclass
class AlertData:
    id_: int
    created_by: UserCustom
    repeat_interval: int  # Interval in days
    event_name: str
    next_time: datetime

    def __lt__(self, other):
        if isinstance(other, AlertData):
            return self.next_time < other.next_time
        return NotImplemented

    def alert_text(self):
        return f'{self.event_name} starts at {self.next_time}'

    def advance_alert_time(self):
        self.next_time += self.repeat_interval
