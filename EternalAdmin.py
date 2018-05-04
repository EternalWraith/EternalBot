import discord
import sqlite3 as database

from discord.ext import commands

class Admin:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='prefix', brief="I'll change your prefix for you... but then again, maybe I won't >:3")
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, *, text: str):
        conn = database.connect(DBNAME)
        config = conn.cursor()
        print("Setting Prefix of {0} to {1}".format(ctx.guild, text))
        config.execute("""
    UPDATE server_{0} SET Prefix = "{1}"
    """.format(ctx.guild.id, text))
        conn.commit()
        conn.close()
        upload(DBNAME)
        await ctx.send("Prefix for {0} has been changed to {1}!".format(ctx.guild, text))

    @commands.command(name='settings')
    @commands.has_permissions(administrator=True)
    async def settings(self, ctx, *, text: str):
        command, text, value = text.split(" ")
        editable = { "work" : 0 }
        editable["work"] = { "Location" : DBNAME, "Table" : "server_{0}".format(ctx.guild.id), "Where": False }
        editable["work"]["Options"] = {"max": {"ID": "MaxWork"}, "min": {"ID": "MinWork"}, "wait": {"ID": "WorkCooldown"} }
        editable["work"]["Options"]["max"]["Message"] = "Set the max payout for working to {0}".format(value)
        editable["work"]["Options"]["min"]["Message"] = "Set the min payout for working to {0}".format(value)
        editable["work"]["Options"]["wait"]["Message"] = "Set the waiting time between working to {0} minutes".format(value)
        if command in editable:
            if text in editable[command]["Options"]:
                conn = database.connect(editable[command]["Location"])
                config = conn.cursor()
                if editable[command]["Where"]:
                    pass
                else:
                    config.execute("""
    UPDATE {0} SET {1} = {2}
    """.format(editable[command]["Table"],editable[command]["Options"][text]["ID"],value))
                conn.commit()
                conn.close()
                upload(editable[command]["Location"])
                await ctx.send(editable[command]["Options"][text]["Message"])
            else:
                await ctx.send("{0} is not an available option for {1}".format(text,command))
        else:
            await ctx.send("{0} is not an editable command".format(command))

def setup(bot):
    bot.add_cog(Admin(bot))
