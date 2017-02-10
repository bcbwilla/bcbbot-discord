import logging
import socket
import argparse
import asyncio
import requests

from mcstatus import MinecraftServer
import discord

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

parser = argparse.ArgumentParser(description='bcbbot lurks')
parser.add_argument('--token', type=str, help='bot login token')


def get_status():
    response = requests.get('http://status.mojang.com/check')
    if not response.ok:
        return

    # merge list of dicts into one dict
    services = {}
    for service_data in response.json():
        services.update(service_data)

    return services


def format_status_message(services):

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


client = discord.Client()


@client.event
async def on_ready():
    logger.info('Logged in as {}.'.format(client.user.name))
    logger.info('Connected to: {}'.format([s.name for s in client.servers]))


@client.event
async def on_message(message):
    if client.user == message.author:
        logger.info('Bot message, ignoring.')
        return

    content, channel = message.content, message.channel
    if content.startswith('!test'):
        await client.send_message(channel, '( ͡° ͜ʖ ͡°)')

    elif content.startswith('!ok'):
        msg = await client.send_message(channel, 'haha')
        for laugh in ['lol', 'great job']:
            await asyncio.sleep(0.8)
            msg = await client.edit_message(msg, laugh)

        await asyncio.sleep(1)
        await client.delete_message(msg)

    elif content.startswith('!mcstatus'):
        statuses = get_status()
        if not statuses:
            msg = "Can't get Minecraft servers status."
        else:
            msg = 'Status of Minecraft servers:\n{}'.format(format_status_message(statuses))
        await client.send_message(channel, msg)

    elif content.startswith('!mcping') and len(content.split(' ')) > 1:
        ip = content.split(' ')[1]

        server = MinecraftServer.lookup(ip)
        try:
            status = server.status()
            await client.send_message(channel, '**{0}**: {1} players online. Running {2}'.format(
                      ip, status.players.online, status.version.name))
        except socket.gaierror:
            await client.send_message(channel, 'Cannot reach server.')


@client.event
async def on_server_join(server):
    await client.send_message(server, "Hi guys I'm a bot beep boop. I SAID BEEP BOOP ( ͡° ͜ʖ ͡°)")


if __name__ == '__main__':
    args = parser.parse_args()
    client.run(args.token)
