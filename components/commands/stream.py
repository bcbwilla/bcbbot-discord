import requests

from components.bot import bot


def get_live_stream(channel):
    base_url = 'https://api.twitch.tv/kraken/'
    response = requests.get(base_url + 'streams/{}'.format(channel))
    if response.ok and response.json().get('stream'):
        return 'http://www.twitch.tv/{}'.format(channel)


@bot.command()
async def streaming(channel):
    """ Get status of Twitch stream 'channel' """

    stream = get_live_stream(channel)
    if stream:
        await bot.say('{} is online! {}'.format(channel, stream))
    else:
        await bot.say('{} is not currently streaming.'.format(channel))
