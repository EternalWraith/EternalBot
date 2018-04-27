#NDM4Nzc1Mjc1MDE1MTEwNjY2.DcJtxw.8U1TRxkhnLEkRHvqF8YcWztUeGc
import discord
import sqlite3 as database
from discord.ext import commands

__version__="0.0.0"

def get_prefix(bot, message):
    prefixes = {}

    readthem = conn.cursor()
    try:
        readthem.execute("SELECT * FROM Servers")

        server_list = readthem.fetchall()
        print(server_list)
        for row in server_list:
            readthem.execute("SELECT Prefix FROM server_{0}".format(row[1]))
            prefixes[row[1]] = readthem.fetchall()[0][0]

        print(prefixes)
        if not message.guild:
            return '?'
        else:
            return commands.when_mentioned_or(prefixes[message.guild.id])(bot, message)
    except:
        return commands.when_mentioned_or("e!")(bot, message)

conn = database.connect("config.db")
config = conn.cursor()
bot = commands.Bot(command_prefix=get_prefix, description='Eternal Bot')


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

    await bot.process_commands(message)

@bot.event
async def on_guild_join(ctx):
    config.execute("""
CREATE TABLE server_{0} (
    Prefix varchar(255)
);
""".format(ctx.id))
    config.execute("""
INSERT INTO server_{0} (Prefix) VALUES ("e!");
""".format(ctx.id))
    config.execute("""
INSERT INTO Servers (ServerID) VALUES ({0});
""".format(ctx.id))
    conn.commit()
    print("Joined {0}".format(ctx.name))
    
@bot.event
async def on_guild_remove(ctx):
    config.execute("""
DROP TABLE server_{0};
""".format(ctx.id))
    conn.commit()
    print("Left {0}".format(ctx.name))

@bot.command(name='ping') #brief="Ping me, I'll Pong you right back! >:3"
async def ping(ctx):
    await ctx.send("Pong! *(psst, stats for the nerds! {0}, {1})*".format(ctx.channel,ctx.channel.id))

@bot.command(name='communism') #brief='Cyka Blayt Bratukha! Rush B {-}7'
async def communism(ctx):
    await ctx.channel.send('☭')
    await ctx.message.delete()

@bot.command(name='pfp') #brief="Hey! Baka! Why you looking at other people's profile pictures? Hmmm?"
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

@bot.command(name='prefix')
async def prefix(ctx, *, text: str):
    print("Setting Prefix of {0} to {1}".format(ctx.guild, text))
    config.execute("""
UPDATE server_{0} SET Prefix = "{1}"
""".format(ctx.guild.id, text))

@bot.command(name='setup')
async def setup(ctx):
    if ctx.message.author.id == 270480523833507850:
        config.execute("""
    CREATE TABLE Servers (
        ID int AUTO_INCREMENT,
        ServerID int
    );
    """)
        print("Setup first time database")
        conn.commit()
    else:
        await ctx.send("Sorry, you don't have permission to use this command! Only Daddy Eternal has permission to use this!")

@bot.command(name='repair')
async def repair(ctx):
    if ctx.message.author.id == 270480523833507850:
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
    Prefix varchar(255)
);
""".format(ctx.guild.id))
                config.execute("""
INSERT INTO server_{0} (Prefix) VALUES ("e!");
""".format(ctx.guild.id))
                config.execute("""
INSERT INTO Servers (ServerID) VALUES ({0});
""".format(ctx.guild.id))
                conn.commit()
            except:
                print("Could not create table... for some reason \_(^-^)_/")
    else:
        await ctx.send("Sorry, you don't have permission to use this command! Only Daddy Eternal has permission to use this!")



#DO NOT REMOVE THIS, EVERYTHING MUST BE ABOVE THIS
bot.run('NDM4Nzc1Mjc1MDE1MTEwNjY2.DcJtxw.8U1TRxkhnLEkRHvqF8YcWztUeGc')
