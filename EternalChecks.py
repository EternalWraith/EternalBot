import discord

from discord.ext import commands


def bot_control():
    async def predicate(ctx):
        return ctx.author.guild_permissions.administrator
    return commands.check(predicate)
