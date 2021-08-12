from datetime import datetime

from discord.ext import commands, tasks

from bot.alert.alert import Alert
from bot.common.cog_common import CogCommon
from bot.common.user_custom import UserCustom
from conf import Conf, DBKeys
from utils import db_cache
from utils.log import log

conf = Conf.Alert
"""Map class with setting for this cog to variable"""


class CogAlert(CogCommon, name='Alert'):
    data: Alert  # Specify type of attribute for linting

    def __init__(self, db: db_cache, bot):
        super().__init__(db, conf=conf, db_key=DBKeys.ALERT,
                         data_def_constructor=Alert)
        self.bot = bot
        self.poll_alerts.start()

    @tasks.loop(seconds=conf.ALERT_POLL_INTERVAL)
    async def poll_alerts(self):
        if await self.data.check_next_alert(self.bot):
            # Save if an alert was sent
            self.save()
        if self.data.next_alert is None:
            log('No pending Alerts - Polling Stopping')
            self.poll_alerts.cancel()

    @poll_alerts.before_loop
    async def before_poll_alerts(self):
        await self.bot.wait_until_ready()

    ##########################################################################
    # BASE GROUP
    @commands.group(**conf.BASE_GROUP)
    async def base(self, ctx):
        await super().base(ctx)

    ##########################################################################
    # NORMAL COMMANDS
    @base.command(**conf.Command.DISPLAY)
    async def display(self, ctx):
        await self.send_data_str(ctx,
                                 f'Alerts sent {self.data.lead_time} minutes '
                                 f'before alert.')

    ##########################################################################
    # PRIVILEGED COMMANDS
    @base.command(**conf.Command.CREATE)
    @commands.has_any_role(*conf.Permissions.PRIV_ROLES)
    async def create(self, ctx, interval_in_days: int, next_time: str,
                     name: str):
        next_time = datetime.fromisoformat(next_time)
        self.data.create(
            UserCustom.get_user_custom(ctx.author),
            interval_in_days,
            name,
            next_time)
        self.save()
        await self.send_data_str(ctx, f'New alert "{name}" added.')

        # Ensure the timer is started
        if not self.poll_alerts.is_running():
            self.poll_alerts.start()

    @base.command(**conf.Command.REMOVE)
    @commands.has_any_role(*conf.Permissions.PRIV_ROLES)
    async def remove(self, ctx, alert_id: int):
        self.data.remove(alert_id)
        self.save()
        await self.send_data_str(ctx, f'Alert With ID: {alert_id} removed')

    @base.command(**conf.Command.SET_LEAD)
    @commands.has_any_role(*conf.Permissions.PRIV_ROLES)
    async def set_lead(self, ctx, lead_time_in_min: int):
        self.data.set_lead_time(lead_time_in_min)
        self.save()
        await ctx.send(
            f'Lead time set to {lead_time_in_min} minutes before the alert')
