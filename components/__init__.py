from .commands import *


async def handle_command(client, message):
    name, *args = message.content[1:].split(' ')
    await COMMAND_REGISTRY[name](client, message)
