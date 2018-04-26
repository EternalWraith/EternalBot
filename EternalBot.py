#NDM4Nzc1Mjc1MDE1MTEwNjY2.DcJtxw.8U1TRxkhnLEkRHvqF8YcWztUeGc
import discord
from discord.ext import commands

__version__="0.0.0"

command_prefix='e!'
description = 'Enter a description here'
bot = commands.Bot(command_prefix)
client = discord.Client()

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name="Nibbling on Cookies", url="http://twitch.tv/megaskull100", type=1), status=discord.Status.dnd)

@client.event
async def on_ready():
    print('Running client')
    await client.change_presence(activity="Nibbling on cookies", status=discord.Status.dnd)

@bot.command(pass_context=True)
async def ping(ctx):
    await ctx.send("Pong!")



bot.run('NDM4Nzc1Mjc1MDE1MTEwNjY2.DcJtxw.8U1TRxkhnLEkRHvqF8YcWztUeGc')
