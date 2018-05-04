#NDM4Nzc1Mjc1MDE1MTEwNjY2.DcJtxw.8U1TRxkhnLEkRHvqF8YcWztUeGc
from __future__ import print_function
import discord, random, datetime
import sqlite3 as database

from discord.ext import commands
from EternalCloudStorage import *


__version__="0.0.0"

def get_prefix(bot, message):
    conn = database.connect(DBNAME)
    config = conn.cursor()
    prefixes = {}

    readthem = conn.cursor()
    try:
        readthem.execute("SELECT * FROM Servers")

        server_list = readthem.fetchall()
        #print(server_list)
        for row in server_list:
            readthem.execute("SELECT Prefix FROM server_{0}".format(row[1]))
            prefixes[row[1]] = readthem.fetchall()[0][0]

        #print(prefixes)
        conn.close()
        if not message.guild:
            return '?'
        else:
            return commands.when_mentioned_or(prefixes[message.guild.id])(bot, message)
    except:
        return commands.when_mentioned_or("e!")(bot, message)

DBNAME = "config.db"
bot = commands.Bot(command_prefix=get_prefix, description='Eternal Bot')
bot.load_extension("EternalCurrency")


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    download_all()
    await bot.change_presence(activity=discord.Game(name="Nibbling on Cookies", type=1, url="http://twitch.tv/megaskull100"))

@bot.event
async def on_message(message):
    if message.content.count("<@{0.user.id}>".format(bot)) > 0:
        await message.channel.send("Baka! Why are you pinging me {0.author.mention}?! Can't you see I am trying to eat cookies? >:(".format(message))

    if message.content.startswith("e!test"):
        await message.channel.send(str(message.channel.id))

    await bot.process_commands(message)

@bot.event
async def on_guild_join(ctx):
    print("Joined {0}".format(ctx.name))
    SERVERDB = "{0}.db".format(ctx.id)
    conn = database.connect(DBNAME)
    config = conn.cursor()
    config.execute("""
CREATE TABLE server_{0} (
    Prefix varchar(255),
    WorkCooldown int,
    MaxWork int,
    MinWork int
);
""".format(ctx.id))
    config.execute("""
INSERT INTO server_{0} (Prefix, WorkCooldown, MaxWork, MinWork) VALUES ("e!", 240, 100, 50);
""".format(ctx.id))
    config.execute("""
INSERT INTO Servers (ServerID) VALUES ({0});
""".format(ctx.id))
    conn.commit()
    print("Joined {0}".format(ctx.name))
    conn.close()
    upload(DBNAME)
    conn = database.connect(SERVERDB)
    config = conn.cursor()
    config.execute("""
    CREATE TABLE Money (
        ID int AUTO_INCREMENT,
        UserID int,
        Wallet int,
        Bank int,
        LastWork varchar(255)
    );
    """)
    conn.commit()
    conn.close()
    upload(SERVERDB)
    
@bot.event
async def on_guild_remove(ctx):
    conn = database.connect(DBNAME)
    config = conn.cursor()
    config.execute("""
DROP TABLE server_{0};
""".format(ctx.id))
    conn.commit()
    conn.close()
    upload(DBNAME)
    print("Left {0}".format(ctx.name))

@bot.command(name='ping', brief="Ping me, I'll Pong you right back! >:3")
async def ping(ctx):
    await ctx.send("Pong! *(psst, stats for the nerds! {0}, {1})*".format(ctx.channel,ctx.channel.id))

@bot.command(name='communism') #brief='Cyka Blayt Bratukha! Rush B {-}7'
async def communism(ctx):
    await ctx.channel.send('☭')
    await ctx.message.delete()

@bot.command(name='pfp', brief="Hey! Baka! Why you looking at other people's profile pictures? Hmmm?")
async def pfp(ctx, *, user: discord.User):
    em = discord.Embed()
    em.set_image(url=user.avatar_url)
    await ctx.channel.send(embed=em)

@bot.command(name='invite')
async def invite(ctx):
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
        app_info = await bot.application_info()
        await ctx.send("Here you go friend! One invite just for you!\n{0}"
                           .format(discord.utils.oauth_url(app_info.id, perms)))

@bot.command(name='prefix', brief="I'll change your prefix for you... but then again, maybe I won't >:3")
@commands.has_permissions(administrator=True)
async def prefix(ctx, *, text: str):
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

@bot.command(name='setup', hidden=True)
async def setup(ctx):
    if ctx.message.author.id == 270480523833507850:
        conn = database.connect(DBNAME)
        config = conn.cursor()
        try: config.execute("DROP TABLE Servers")
        except: print("No table to delete")
        config.execute("""
    CREATE TABLE Servers (
        ID int AUTO_INCREMENT,
        ServerID int
    );
    """)
        print("Setup first time database")
        conn.commit()
        conn.close()
        upload(DBNAME)
        await ctx.send("Database has been set up!")
    else:
        await ctx.send("Sorry, you don't have permission to use this command! Only Daddy Eternal has permission to use this!")

@bot.command(name='repair', hidden=True)
async def repair(ctx):
    SERVERDB = "{0}.db".format(ctx.guild.id)
    conn = database.connect(DBNAME)
    config = conn.cursor()
    if ctx.message.author.id == 270480523833507850:
            SERVERDB = "{0}.db".format(ctx.guild.id)
            try:
                config.execute("""
DROP TABLE server_{0};
""".format(ctx.guild.id))
            except:
                print("No table to delete")
            conn.commit()
            try:
                config.execute("""
CREATE TABLE server_{0} (
    Prefix varchar(255),
    WorkCooldown int,
    MaxWork int,
    MinWork int
);
""".format(ctx.guild.id))
                config.execute("""
INSERT INTO server_{0} (Prefix, WorkCooldown, MaxWork, MinWork) VALUES ("e!", 240, 100, 50);
""".format(ctx.guild.id))
                config.execute("""
INSERT INTO Servers (ServerID) VALUES ({0});
""".format(ctx.guild.id))
                conn.commit()
                conn.close()
                
                conn = database.connect(SERVERDB)
                config = conn.cursor()
                try:
                    config.execute("""
DROP TABLE Money;
""")
                except:
                   print("No table to delete")
                config.execute("""
                CREATE TABLE Money (
                    ID int AUTO_INCREMENT,
                    UserID int,
                    Wallet int,
                    Bank int,
                    LastWork varchar(255)
                );
                """)
                conn.commit()
                conn.close()
                await ctx.send("Database repaired for your server!")
            except:
                await ctx.send("Failed to repair database. Please contact <@270480523833507850> for help!")
                print("Could not create table... for some reason \_(^-^)_/")
            upload(DBNAME)
            upload(SERVERDB)
    else:
        await ctx.send("Sorry, you don't have permission to use this command! Only Daddy Eternal has permission to use this!")





@bot.command(name='settings')
@commands.has_permissions(administrator=True)
async def settings(ctx, *, text: str):
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

#DO NOT REMOVE THIS, EVERYTHING MUST BE ABOVE THIS
bot.run('NDM4Nzc1Mjc1MDE1MTEwNjY2.DcJtxw.8U1TRxkhnLEkRHvqF8YcWztUeGc')
