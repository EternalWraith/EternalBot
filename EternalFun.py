import discord

from discord.ext import commands

class Fun:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping', brief="Ping me, I'll Pong you right back! >:3")
    async def ping(self, ctx):
        await ctx.send("Pong! *(psst, stats for the nerds! {0}, {1})*".format(ctx.channel,ctx.channel.id))

    @commands.command(name='communism') #brief='Cyka Blayt Bratukha! Rush B {-}7'
    async def communism(self, ctx):
        await ctx.channel.send('☭')
        await ctx.message.delete()

    @commands.command(name='pfp', brief="Hey! Baka! Why you looking at other people's profile pictures? Hmmm?")
    async def pfp(self, ctx, *, user: discord.User):
        em = discord.Embed()
        em.set_image(url=user.avatar_url)
        await ctx.channel.send(embed=em)


def setup(bot):
    bot.add_cog(Fun(bot))
