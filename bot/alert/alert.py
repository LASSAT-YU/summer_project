from datetime import datetime
from typing import List

from discord.ext import commands

from bot.alert.alert_data import AlertData
from bot.common.user_custom import UserCustom


class Alert:
    def __init__(self):
        self.data: List[AlertData] = []
        self.next_alert = None
        self.next_id = 0

    def create(self, user: UserCustom, repeat_interval: int, name: str,
               next_time: datetime):
        self.data.append(
            AlertData(self.get_next_id(), user, repeat_interval, name,
                      next_time))
        self.find_next_event()

    def remove(self, id_):
        element_to_rem = None
        for alert in self.data:
            if alert.id_ is id_:
                element_to_rem = alert
                break
        if element_to_rem is None:
            raise commands.errors.UserInputError(
                f'No alert found with id {id_}')
        else:
            self.data.remove(element_to_rem)
            if element_to_rem == self.next_alert:
                self.find_next_event()

    def find_next_event(self):
        if len(self.data) <= 0:
            self.next_alert = None
        else:
            next_alert = self.data[0]
            for alert in self.data:
                if alert < next_alert:
                    next_alert = alert
            self.next_alert = next_alert

    def get_next_id(self):
        result = self.next_id
        self.next_id += 1
        return result

    def __str__(self):
        return f'Alerts: {self.data}'
