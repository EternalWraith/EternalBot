#NDM4Nzc1Mjc1MDE1MTEwNjY2.DcJtxw.8U1TRxkhnLEkRHvqF8YcWztUeGc
import discord
from discord.ext import commands

__version__="0.0.0"

prefix="e!"
description = 'Enter a description here'
bot = commands.Bot(prefix)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name="Nibbling on Cookies", type=1, url="http://twitch.tv/megaskull100"))

@bot.event
async def on_message(message):
    if message.content.count("<@{0.user.id}>".format(bot)) > 0:
        await message.channel.send("Baka! Why are you pinging me {0.author.mention}?! Can't you see I am trying to eat cookies? >:(".format(message))

    if message.content.startswith("e!test"):
        await message.channel.send(str(message.channel.id))

@bot.command(brief="Ping me, I'll Pong you right back! >:3")
async def ping(ctx):
    await ctx.send("Pong! *(psst, stats for the nerds! {0}, {1})*".format(ctx.channel,ctx.channel.id))


"""

"""

#Bestest's stuff
@bot.command(brief='Cyka Blayt Bratukha! Rush B {-}7')
async def communism(ctx):
        await ctx.channel.send('☭')
        await ctx.message.delete()

@bot.command(brief="Hey! Baka! Why you looking at other people's profile pictures? Hmmm?")
async def pfp(ctx, *, user: discord.User):
        em = discord.Embed()
        em.set_image(url=user.avatar_url)
        await ctx.channel.send(embed=em)


#DO NOT REMOVE THIS, EVERYTHING MUST BE ABOVE THIS
bot.run('NDM4Nzc1Mjc1MDE1MTEwNjY2.DcJtxw.8U1TRxkhnLEkRHvqF8YcWztUeGc')
