import logging
from datetime import datetime, timedelta
from typing import List

from discord.ext import commands

from bot.alert.alert_data import AlertData
from bot.common.user_custom import UserCustom
from conf import Conf
from utils.log import log


class Alert:
    def __init__(self):
        self.lead_time = 60
        self.data: List[AlertData] = []
        self._next_alert = None
        self._next_alert_target = None
        self.next_id = 0

    def create(self, user: UserCustom, repeat_interval: int, name: str,
               next_time: datetime):
        if repeat_interval < 0:
            raise commands.errors.UserInputError(
                f'Repeat interval must be 0 for once only or greater but '
                f'{repeat_interval} received')
        self.data.append(
            AlertData(self.get_next_id(), user,
                      timedelta(days=repeat_interval), name,
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

    def set_lead_time(self, value: int):
        self.lead_time = value

    def find_next_event(self):
        if len(self.data) <= 0:
            self.next_alert = None
        else:
            next_alert = self.data[0]
            for alert in self.data:
                if alert < next_alert:
                    next_alert = alert
            self.next_alert = next_alert

    async def check_next_alert(self, bot) -> bool:
        """
        Checks to see if the next alert should be fired now
        :param bot: handle to the bot to use to send the message
        :return: True if an alert was fired else false
        """
        result = False
        try:
            if self._next_alert_target is not None:
                if datetime.now() > self._next_alert_target:
                    channel = bot.get_channel(Conf.Alert.ALERT_CHANNEL_ID)
                    await channel.send(self.next_alert.alert_text())
                    result = True
                    self.next_alert.advance_alert_time()
                    if self.next_alert.expired:
                        log(f'Alert Expired: {self.next_alert}')
                        self.remove(self.next_alert.id_)
                    self.find_next_event()
            return result
        except Exception as e:
            log(f'Exception checking next alert: {e}', logging.ERROR)
            return False

    def get_next_id(self):
        result = self.next_id
        self.next_id += 1
        return result

    def __str__(self):
        result = f'Alerts:\n'
        for alert in self.data:
            result += f'- {alert}\n'
        result += '---'
        return result

    @property
    def next_alert(self):
        return self._next_alert

    @next_alert.setter
    def next_alert(self, value):
        self._next_alert = value
        if value is None:
            self._next_alert_target = None
        else:
            self._next_alert_target = self.next_alert.next_time \
                                      - timedelta(minutes=self.lead_time)
