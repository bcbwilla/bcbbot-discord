"""
Misc simple commands
"""

from components.bot import bot


@bot.command()
async def add(left, right):
    """Adds two numbers together."""
    await bot.say(left + right)


@bot.command()
async def hi():
    """ Says 'hi' """
    await bot.say('hi')


@bot.command()
async def test():
    """ Ping """
    await bot.say('( ͡° ͜ʖ ͡°)')
