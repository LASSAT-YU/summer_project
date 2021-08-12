from datetime import datetime

from discord.ext import commands

from bot.alert.alert import Alert
from bot.common.cog_common import CogCommon
from bot.common.user_custom import UserCustom
from conf import Conf, DBKeys
from utils import db_cache

conf = Conf.Alert
"""Map class with setting for this cog to variable"""


class CogAlert(CogCommon, name='Alert'):
    data: Alert  # Specify type of attribute for linting

    def __init__(self, db: db_cache):
        super().__init__(db, conf=conf, db_key=DBKeys.ALERT,
                         data_def_constructor=Alert)

    ##########################################################################
    # BASE GROUP
    @commands.group(**conf.BASE_GROUP)
    async def base(self, ctx):
        await super().base(ctx)

    ##########################################################################
    # NORMAL COMMANDS
    @base.command(**conf.Command.DISPLAY)
    async def display(self, ctx):
        await self.send_data_str(ctx)

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

    @base.command(**conf.Command.REMOVE)
    @commands.has_any_role(*conf.Permissions.PRIV_ROLES)
    async def remove(self, ctx, alert_id: int):
        self.data.remove(alert_id)
        self.save()
        await self.send_data_str(ctx, f'Alert With ID: {alert_id} removed')
