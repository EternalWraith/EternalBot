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

    @commands.command(name='invite')
    async def invite(self, ctx):
            perms = discord.Permissions.none()
            perms.read_messages = True
            perms.send_messages = True
            perms.manage_roles = True
            perms.ban_members = True
            perms.kick_members = True
            perms.manage_messages = True
            perms.embed_links = True
            perms.read_message_history = True
            perms.attach_files = True
            app_info = await commands.application_info()
            await ctx.send("Here you go friend! One invite just for you!\n{0}"
                               .format(discord.utils.oauth_url(app_info.id, perms)))


def setup(bot):
    bot.add_cog(Fun(bot))
