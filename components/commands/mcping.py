import socket

from mcstatus import MinecraftServer

from components.bot import bot


@bot.command()
async def mcping(ip):
    """ Get status of Minecraft server 'ip' """

    server = MinecraftServer.lookup(ip)
    try:
        status = server.status()
        await bot.say('**{0}**: {1} players online. Running {2}'.format(
                  ip, status.players.online, status.version.name))
    except socket.gaierror:
        await bot.say('Cannot reach server.')
