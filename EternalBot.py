#NDM4Nzc1Mjc1MDE1MTEwNjY2.DcJtxw.8U1TRxkhnLEkRHvqF8YcWztUeGc
from __future__ import print_function
import discord, os, io
import sqlite3 as database
from discord.ext import commands

from apiclient.discovery import build
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
from httplib2 import Http
from oauth2client import file, client, tools

__version__="0.0.0"

def get_prefix(bot, message):
    conn = database.connect(DBNAME)
    config = conn.cursor()
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
        conn.close()
        if not message.guild:
            return '?'
        else:
            return commands.when_mentioned_or(prefixes[message.guild.id])(bot, message)
    except:
        return commands.when_mentioned_or("e!")(bot, message)

DBNAME = "config.db"
bot = commands.Bot(command_prefix=get_prefix, description='Eternal Bot')
filestorage = {}

SCOPES = 'https://www.googleapis.com/auth/drive'
store = file.Storage('login.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('drive', 'v3', http=creds.authorize(Http()))

def upload(filename):
    metadata = {'name': filename}
    if filename in filestorage:
        file_id = filestorage[filename]
        file = service.files().get(fileId=file_id).execute()
        media_body = MediaFileUpload(
        filename, mimetype='application/x-sqlite3', resumable=True)

        updated_file = service.files().update(
        fileId=file_id,
        #body=file,
        media_body=media_body).execute()
    else:
        media = MediaFileUpload(filename,
                            mimetype='application/x-sqlite3')
        file = service.files().create(body=metadata,
                                        media_body=media,
                                        fields='id').execute()
        filestorage[filename] = file["id"]
    print('Uploaded "%s"' % (filename))

def download(file_name, file_id):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    print('Downloaded "%s" (%s)' % (file_name, file_id))
    contents = fh.getvalue()
    outf = open(file_name, "wb")
    outf.write(contents)
    outf.close()
    filestorage[file_name] = file_id

def download_all():
    items = []
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items += results.get('files', [])
    token = results.get('nextPageToken', None)
    while token != None:
        results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items += results.get('files', [])
        token = results.get('nextPageToken', None)
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            download(item['name'], item['id'])

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
    conn = database.connect(DBNAME)
    config = conn.cursor()
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
    conn.close()
    upload(DBNAME)
    conn = database.connect(DBNAME)
    
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
    conn = database.connect(DBNAME)
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
    conn = database.connect(DBNAME)
    config = conn.cursor()
    print("Setting Prefix of {0} to {1}".format(ctx.guild, text))
    config.execute("""
UPDATE server_{0} SET Prefix = "{1}"
""".format(ctx.guild.id, text))
    conn.commit()
    conn.close()
    upload(DBNAME)
    conn = database.connect(DBNAME)

@bot.command(name='setup')
async def setup(ctx):
    if ctx.message.author.id == 270480523833507850:
        conn = database.connect(DBNAME)
        config = conn.cursor()
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
        conn = database.connect(DBNAME)
    else:
        await ctx.send("Sorry, you don't have permission to use this command! Only Daddy Eternal has permission to use this!")

@bot.command(name='repair')
async def repair(ctx):
    conn = database.connect(DBNAME)
    config = conn.cursor()
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
            conn.close()
            upload(DBNAME)
            conn = database.connect(DBNAME)
    else:
        await ctx.send("Sorry, you don't have permission to use this command! Only Daddy Eternal has permission to use this!")



#DO NOT REMOVE THIS, EVERYTHING MUST BE ABOVE THIS
bot.run('NDM4Nzc1Mjc1MDE1MTEwNjY2.DcJtxw.8U1TRxkhnLEkRHvqF8YcWztUeGc')
