import logging

from discord.ext import commands

logger = logging.getLogger('discord')


class Bcbbot(commands.Bot):
    """ The bot """

    def __init__(self, command_prefix, description):
        super().__init__(command_prefix=command_prefix, description=description)

    async def on_ready(self):
        logger.info('Logged in as {}.'.format(self.user.name))
        logger.info('Connected to: {}'.format([s.name for s in self.servers]))

    async def on_server_join(self, server):
        logger.info('Joined server {}'.format(server))
        await self.send_message(server.default_channel,
                                "Hi guys I'm a bot beep boop."
                                " I SAID BEEP BOOP ( ͡° ͜ʖ ͡°)")


bot = Bcbbot(command_prefix='!', description='''The cutest robot''')


