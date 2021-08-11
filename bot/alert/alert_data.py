from dataclasses import dataclass
from datetime import datetime

from bot.common.user_custom import UserCustom


@dataclass
class AlertData:
    _id: int
    created_by: UserCustom
    repeat_interval: int
    event_name: str
    next_time: datetime

    def alert_text(self):
        return f'{self.event_name} starts at {self.next_time}'

    def advance_alert_time(self):
        self.next_time += self.repeat_interval
