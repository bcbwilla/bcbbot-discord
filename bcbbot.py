import logging

import argparse

import discord

from components import handle_command

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='bcbbot.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

parser = argparse.ArgumentParser(description='bcbbot lurks')
parser.add_argument('--token', type=str, help='bot login token')
parser.add_argument('--debug', action='store_true')
parser.add_argument('--log-file', type=str, dest='log_file', help='log file')


client = discord.Client()


@client.event
async def on_ready():
    logger.info('Connected to: {}'.format([s.name for s in client.servers]))


@client.event
async def on_message(message):
    if client.user != message.author and message.content.startswith('!'):
        await handle_command(client, message)


@client.event
async def on_server_join(server):
    await client.send_message(server, "Hi guys I'm a bot beep boop. I SAID BEEP BOOP ( ͡° ͜ʖ ͡°)")


if __name__ == '__main__':
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    client.run(args.token)
