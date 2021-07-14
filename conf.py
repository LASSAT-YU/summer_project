import logging
from string import Template


# TODO Add option to chose to use qualifying round instead of alternating byes

class MasterPermissions:
    class PRIV:
        SETTINGS = {'Software'}
        TOP = SETTINGS

    class Channels:
        TOP_ONLY = {'software'}
        TOP = TOP_ONLY
        SETTINGS = TOP


class DBKeys:  # Database key values
    TOURNAMENT = 'tournament'
    UNRANKED = 'unranked'
    REGISTRATION = 'registration'


class Conf:
    BOT_DESCRIPTION = "Bazooka Alliance BOT"
    VERSION = '1.14'
    LOG_LEVEL = logging.INFO
    COMMAND_PREFIX = 'bb'
    SAVE_CACHE_DELAY = 30  # Minimum number of seconds between saves
    EXPORT_FILE_NAME = 'export.yaml'
    EXPORT_DELAY = 15
    URL = 'https://bazooka-bot.one23.repl.co/'
    EMBED_COLOR = 0x373977

    class ENV:  # Environment variable names
        TOKEN = 'TOKEN_LASSAT'

    class TopLevel:
        INTERNAL_CHANNEL_ID = 613723324018720787
        WELCOME_MSG = Template(
                "Welcome ${mention}. Nice to have you here. Make yourself at "
                "home. If you are looking to organize a race tie check out our "
                "<#744875911119110245>. If you are looking to join one of our "
                "alliances please post a screen shot of your previous season "
                "achievements in <#760521977072713758>. Otherwise you're welcome "
                "to just chill or Gents are also welcome to check out our "
                "<#757542001708105739>.")
        MEMBER_LEAVE = Template(
                "Hey, just letting you know I noticed ${name} left the server...")

        class Permissions:
            ALLOWED_DM_COMMANDS = {  # Hard coded to allow for debugging
                    'export',
                    'version',
                    'ping',
            }
            ALLOWED_CHANNELS = MasterPermissions.Channels.TOP
            PRIV_ROLES = MasterPermissions.PRIV.TOP

        class Command:
            DM = {
                    'name': 'dm',
                    'help': 'Sends a DM to the user'}
            PING = {
                    'name': 'ping',
                    'help': 'Tests if the bot is alive. If alive bot responds '
                            'pong'}
            VERSION = {
                    'name': 'version',
                    'hidden': True}
            SAVE = {
                    'name': 'save',
                    'hidden': True}
            EXPORT = {
                    'name': 'export',
                    'hidden': True}

    class Settings:
        class Permissions:
            PRIV_ROLES = MasterPermissions.PRIV.SETTINGS
            ALLOWED_CHANNELS = MasterPermissions.Channels.SETTINGS

