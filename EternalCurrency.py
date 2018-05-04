import discord, random, datetime
import sqlite3 as database

from discord.ext import commands
from EternalCloudStorage import *

DBNAME = "config.db"

class Currency:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='work', brief="Soon you'll be rolling in those delicious cookies :3 Mmmmmm cookies...")
    @commands.guild_only()
    async def work(self, ctx):
        global upload
        conn = database.connect(DBNAME)
        config = conn.cursor()
        config.execute("SELECT WorkCooldown, MaxWork, MinWork FROM server_{0}".format(ctx.guild.id))
        cooldown, maxwork, minwork = config.fetchall()[0]
        conn.close()
        
        conn = database.connect("{0}.db".format(ctx.guild.id))
        config = conn.cursor()
        config.execute("SELECT Wallet, Bank, LastWork FROM Money WHERE UserID={0}".format(ctx.author.id))
        money = config.fetchall()
        gained = random.randint(minwork, maxwork)
        timework = "{0} {1} {2} {3} {4} {5}".format(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day,datetime.datetime.now().hour,datetime.datetime.now().minute,datetime.datetime.now().second)
        now = datetime.datetime(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day,datetime.datetime.now().hour,datetime.datetime.now().minute,datetime.datetime.now().second)

        if len(money) > 0:
            if money[0][2] != "Never":
                splitup = money[0][2].split(" ")
                then = datetime.datetime(int(splitup[0]),int(splitup[1]),int(splitup[2]),int(splitup[3]),int(splitup[4]),int(splitup[5]))

        if len(money) > 0:
            diff = now-then
            #print(diff, now, then)
            if money[0][2] == "Never" or ( diff.seconds/60 >= cooldown and diff.days == 0 ) or diff.days >= 1  :
                wallet = money[0][0]
                bank = money[0][1]
                config.execute("""
        UPDATE Money SET Wallet = {1}, LastWork = "{2}" WHERE UserID = {0}
        """.format(ctx.author.id, wallet+gained, timework))
                await ctx.send("You earned :cookie:{0}! Good job!".format(gained))
            else:
                await ctx.send("You can work again in {0} minutes!".format( round(cooldown-diff.seconds/60)) )
        else:
            config.execute("""
        INSERT INTO Money (UserID, Wallet, Bank, LastWork) VALUES ({0}, {2}, {1}, "{3}");
        """.format(ctx.author.id, 0, gained, timework))
            await ctx.send("You earned :cookie:{0}! Good job!".format(gained))
        conn.commit()
        conn.close()
        upload("{0}.db".format(ctx.guild.id))

    @commands.command(name='balance', brief="This checks how many cookies you have. Warning: If you have too many I may need to rob you >:3")
    @commands.guild_only()
    async def balance(self, ctx, *, user: discord.User=None):
        if user == None:
            user = ctx.author
        conn = database.connect("{0}.db".format(ctx.guild.id))
        config = conn.cursor()
        config.execute("SELECT Wallet, Bank FROM Money WHERE UserID={0}".format(user.id))
        money = config.fetchall()
        if len(money) == 0:
            wallet = 0
            bank = 0
            config.execute("""
    INSERT INTO Money (UserID, Wallet, Bank, LastWork) VALUES ({0}, {1}, {1}, "Never");
    """.format(user.id, 0))
        else:
            wallet = money[0][0]
            bank = money[0][1]
        embed = discord.Embed(title="Balance of {0}".format(user.name), color=0x00ff00)
        embed.add_field(name="Wallet", value=":cookie:"+str(wallet), inline=False)
        embed.add_field(name="Bank", value=":cookie:"+str(bank), inline=False)
        await ctx.channel.send(embed=embed)
        conn.commit()
        conn.close()
        upload("{0}.db".format(ctx.guild.id))

    @commands.command(name='deposit', brief="Put your cookies in a safe place so nobody can steal them (except me...)")
    @commands.guild_only()
    async def deposit(self, ctx, *, text: str="All"):
        conn = database.connect("{0}.db".format(ctx.guild.id))
        config = conn.cursor()
        config.execute("SELECT Wallet, Bank FROM Money WHERE UserID={0}".format(ctx.author.id))
        wallet, bank = config.fetchall()[0]
        try:
            amount = int(text)
        except:
            amount = wallet
        if amount > wallet: amount = wallet
        config.execute("""
        UPDATE Money SET Wallet = {1}, Bank = {2} WHERE UserID = {0}
        """.format(ctx.author.id, wallet-amount, bank+amount))
        await ctx.send("You deposited {0}!".format(amount))
        conn.commit()
        conn.close()

    @commands.command(name='withdraw', brief="Take your cookies out of a safe place, so everyone can rob them. But if someone fails to rob you, you get their cookies")
    @commands.guild_only()
    async def withdraw(self, ctx, *, text: str="All"):
        conn = database.connect("{0}.db".format(ctx.guild.id))
        config = conn.cursor()
        config.execute("SELECT Wallet, Bank FROM Money WHERE UserID={0}".format(ctx.author.id))
        wallet, bank = config.fetchall()[0]
        try:
            amount = int(text)
        except:
            amount = bank
        if amount > bank: amount = bank
        config.execute("""
        UPDATE Money SET Wallet = {1}, Bank = {2} WHERE UserID = {0}
        """.format(ctx.author.id, wallet+amount, bank-amount))
        await ctx.send("You withdrew {0}!".format(amount))
        conn.commit()
        conn.close()


def setup(bot):
    bot.add_cog(Currency(bot))
