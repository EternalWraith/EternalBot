import discord

from discord.ext import commands


def bot_control():
    async def predicate(ctx):
        return ctx.author.guild_permissions.administrator or ctx.author.guild_permissions.manage_channels
    return commands.check(predicate)
