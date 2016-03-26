import requests

from components.bot import bot


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


@bot.command()
async def mcstatus():
    """ Gets the status of Minecraft service servers """

    statuses = get_status()
    if not statuses:
        await bot.say("Can't get Minecraft servers status.")
        return

    message = format_status_message(statuses)
    await bot.say('Status of Minecraft servers:')
    await bot.say(message)
