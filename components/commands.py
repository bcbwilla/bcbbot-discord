import logging
import asyncio
import socket
import requests


from mcstatus import MinecraftServer

logger = logging.getLogger('discord')

COMMAND_REGISTRY = {}


def command(cmd):
    COMMAND_REGISTRY[cmd.__name__.lower()] = cmd()
    return cmd


@command
class Test(object):

    async def __call__(self, client, message):
        await client.send_message(message.channel, '( ͡° ͜ʖ ͡°)')


@command
class OK(object):

    async def __call__(self, client, message):
        msg = await client.send_message(message.channel, 'haha')
        for laugh in ['lol', 'great job']:
            await asyncio.sleep(0.8)
            msg = await client.edit_message(msg, laugh)
        await asyncio.sleep(1)
        await client.delete_message(msg)


@command
class MCPing(object):

    async def __call__(self, client, message):
        ip = message.content.split(' ')[1]

        server = MinecraftServer.lookup(ip)
        try:
            status = server.status()
            await client.send_message(message.channel, '**{0}**: {1} players online. Running {2}'.format(
                      ip, status.players.online, status.version.name))
        except socket.gaierror:
            await client.send_message(message.channel, 'Cannot reach server.')


@command
class Beep(object):

    async def __call__(self, client, message):
        msg = await client.send_message(message.channel, 'USER INPUT "beep" DETECTED.')
        for out in ['LAUNCHING PARSE ENGINE', 'TRAVERSING NATURAL LANGUAGE PARSE TREE', 'INVERTING OPPOSITE BITS',
                    'INTENT IDENTIFIED', 'INITIATING RESPONSE GENERATING RECURSIVE NEURAL NETWORKS', '...',
                    'LOADING OUTPUT INTO OUTPUT PIPE', 'PRINTING RESPONSE PRINTING NOTIFICATION PROMPT', '*CLENCHES*',
                    "'boop' ( ͡° ͜ʖ ͡°)"]:
            await asyncio.sleep(1.7)
            msg = await client.edit_message(msg, out)


@command
class MCStatus(object):

    async def __call__(self, client, message):
        statuses = self.get_status()
        if not statuses:
            msg = "Can't get Minecraft servers status."
        else:
            msg = 'Status of Minecraft servers:\n{}'.format(self.format_status_message(statuses))
        await client.send_message(message.channel, msg)

    def get_status(self):
        response = requests.get('http://status.mojang.com/check')
        if not response.ok:
            return

        # merge list of dicts into one dict
        services = {}
        for service_data in response.json():
            services.update(service_data)

        return services

    def format_status_message(self, services):
        server_name = {
            'minecraft.net': 'Website',
            'account.mojang.com': 'Accounts',
            'authserver.mojang.com': 'Login',
            'sessionserver.mojang.com': 'Sessions',
            'textures.minecraft.net': 'Skins',
            'api.mojang.com': 'API'
        }

        status_map = {
            'green': 'Online',
            'yellow': 'Slow',
            'red': 'OFFLINE',
        }

        message = '```'
        for service, status in services.items():
            if service in server_name.keys():
                message += '{:<10} {:>10}\n'.format(
                    server_name[service]+':', status_map[status])

        message += '```'

        return message

