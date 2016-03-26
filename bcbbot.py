import sys
import logging
import argparse

import yaml

from components.bot import bot
from components.commands import *


logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

parser = argparse.ArgumentParser(description='bcbbot lurks')
parser.add_argument('config', type=str, help='Path to configuration file')


def load_config(filename):
    with open(filename, 'r') as f:
        return yaml.safe_load(f)


def main(bot, config_file):
    try:
        config = load_config(config_file)
        email, password = config.get('email'), config.get('password')
    except IOError as e:
        logger.exception(e)
        sys.exit(1)

    try:
        logger.info('Beep boop good morning.')
        bot.run(email, password)
    except Exception as e:
        logger.exception(str(e))
        logger.info('Shutting down, goodbye.')


if __name__ == '__main__':
    args = parser.parse_args()
    main(bot, args.config)

