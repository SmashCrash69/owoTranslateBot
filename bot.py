import discord, time, random, json
from discord.ext import commands
from Main import owo

subreddits = [
    "dick", 
    "ass", 
    "tits",
    "pussy", 
    "hentai", 
    "bdsm", 
    "porn", 
    "gay_porn",
    "futanari",
    "femboy",
    "thighs",
    "food",
    "cars"]

info = {}
used = {"dick": 0, "ass": 0, "tits": 0, "pussy": 0, "hentai": 0, "bdsm": 0, "porn": 0, "gay_porn": 0, "futanari": 0, "femboy": 0, "thighs": 0, "food": 0, "cars": 0}
prefixes = {}
last_message = {}
helpDescription = """> Bot tag: {0}owo
That command is the basic command to convert
> Bot tag: {0}owo reverse
That command converts back to (or close to) plain english
> Bot tag: {0}owo translate
That command converts without the prefixes and suffixes
> Bot tag: {0}owo help
That command returns this help message"""
settingsHelp = """> Bot tag: {0}settings nsfw
That command toggles nsfw commands
> Bot tag: {0}settings prefix str
That command changes the prefixes (the default "!") to the character (or characters) in the str
> Bot tag: {0}settings admin
That command lists the admins for the bot
> Bot tag: {0}settings admin add _user_
That command adds _user_ to the admins (user must be a ping)
> Bot tag: {0}settings admin remove _user_
That command adds _user_ to the admins (user must be a ping)
> Bot tag: {0}settings help
That command returns this help message"""
spamHelp = "{0}spam dick{1}{0}spam ass{1}{0}spam tits\n{0}spam pussy{1}{0}spam hentai{1}{0}spam bdsm\n{0}spam porn{1}{0}spam gay_porn{1}{0}spam futanari\n{0}spam femboy{1}{0}spam thighs{1}"

def read(urls : dict = {"dick": [], "ass": [], "tits": [], "pussy": [], "hentai": [], "bdsm": [], "porn": [], "gay_porn": [], "futanari": [], "femboy": [], "thighs": [], "food": [], "cars": []}):
    with open("urlsv2.json", "r") as file:
        oldUrls = json.loads(file.read())
        for i in oldUrls:
            if oldUrls[i] != urls[i]:
                if len(oldUrls[i]) > len(urls[i]):
                    urls[i] = oldUrls[i]
    return urls

def store():
    with open("data.json", "w+") as file:
        file.write(json.dumps(info))

def retrieve():
    with open("data.json", "r") as file:
        content = file.read()
        global info
        info = json.loads(content)

def determineprefix(bot, ctx):
    if ctx.guild.name not in info:
        info[ctx.guild.name]["prefix"] = "!"
    return info[ctx.guild.name]["prefix"]

bot = commands.Bot(command_prefix=determineprefix, help_command=None, description="Owofying bot")

@bot.event
async def on_ready():
    retrieve()
    await bot.change_presence(activity=discord.Game(name='with your words, feelings and sexuality'))
    print(f"Logged in as {bot.user} ({bot.user.id})")

@bot.event
async def on_message(ctx):
    if ctx.guild.name not in info:
        if ctx.author.name != bot.user.name:
            info[ctx.guild.name] = {"admin" : [ctx.author.name, "Smash_Crash"], "nsfw" : False, "prefix" : "!"}
            store()
    splitMessage = ctx.content.split(" ")
    if ctx.author != bot.user and splitMessage[0] != "{0}owo".format(info[ctx.guild.name]["prefix"]) and splitMessage[0] != "!settings":
        global last_message
        last_message[f"{ctx.guild.id}/{ctx.channel.id}"] = ctx.channel.last_message_id
    await bot.process_commands(ctx)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    with open("log.txt", "a") as log:
        log.write(f"[{time.asctime(time.localtime(time.time()))}] ({ctx.guild.name}/{str(ctx.channel)}/{str(ctx.author)}) {str(ctx.message.content)} Error: {error}\n")
        await ctx.send(owo(f"Oops, there's been a fucky wucky ({error})"))
        raise error



@bot.command(name="spam")
async def spam(ctx, *, data="random 1"):
    if ctx.invoked_subcommand == None:
        if info[ctx.guild.name]["nsfw"] == False:
            await ctx.send(owo("This feature has been disabled by admins"))
            return
        if not ctx.channel.is_nsfw():
            await ctx.send(owo("This channel is not nsfw, you cannot do this here"))
            return
        async with ctx.typing():
            data = data.split(" ")
            if len(data) > 1:
                try:
                    spam = int(data[1])
                    genre = data[0]
                except Exception as e:
                    if isinstance(e, ValueError):
                        await ctx.send(owo("That isn't a valid choice, see {0}spam".format(info[ctx.guild.name]["prefix"]), translate=True) + " help")
            else:
                try:
                    spam = int(data[0])
                    genre = "random"
                except Exception as e:
                    if isinstance(e, ValueError):
                        spam = 1
                        genre = data[0]

            if genre == "random":
                genre = random.choice(subreddits)
            elif genre not in subreddits:
                if genre == "help":
                    await ctx.send(embed=discord.Embed(title="Settings help", type="rich", description=spamHelp.format(info[ctx.guild.name]["prefix"], ("     " * 2))))     
                    return
                await ctx.send(owo("That isn't a valid choice, see {0}spam".format(info[ctx.guild.name]["prefix"]), translate=True) + " help")
                return
            urls = read()
            await ctx.send("\n".join(urls[genre][used[genre] : (used[genre] + spam)]))
            used[genre] += spam



@bot.group(name="settings")
async def settings(ctx):
    retrieve()
    if ctx.invoked_subcommand is None:
        await ctx.send(
            owo(
                f"Incorrect command, see embed below"), embed=discord.Embed(title="Spam categories", type="rich", description=spamHelp.format(info[ctx.guild.name]["prefix"], ("     " * 2)))
        )

@settings.command()
async def prefix(ctx, *, newprefix):
    with open("log.txt", "a") as log:
        if ctx.author.name in info[ctx.guild.name]["admin"]:
            log.write(f"[{time.asctime(time.localtime(time.time()))}] ({ctx.guild.name}/{str(ctx.channel)}/{str(ctx.author)}) {str(ctx.message.content)}\n")
            info[ctx.guild.name]["prefix"] = newprefix
            await ctx.send(
                owo(
                    f"The prefixes has been changed to {newprefix}")
            )
            log.write(f"[{time.asctime(time.localtime(time.time()))}] Complete\n")
            store()
        else:
            await ctx.send(
                owo(
                    f"You do not have the necessary priviledges")
            )

@settings.command()
async def help(ctx):
    await ctx.send(embed=discord.Embed(title="Settings help", type="rich", description=settingsHelp.format(info[ctx.guild.name]["prefix"])))

@settings.command()
async def nsfw(ctx):
    if ctx.author.name in info[ctx.guild.name]["admin"]:
        if info[ctx.guild.name]["nsfw"]:
            info[ctx.guild.name]["nsfw"] = False
            await ctx.send(owo(f"NSFW content is disabled"))
        else:
            info[ctx.guild.name]["nsfw"] = True
            await ctx.send(owo(f"NSFW content is enabled"))
        store()
    else:
        await ctx.send(
                owo(
                    f"You do not have the necessary priviledges")
            )


@settings.group()
async def admin(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send(owo(", ".join(info[ctx.guild.name]["admin"])))

@admin.command()
async def add(ctx, *, user: discord.User):
    if ctx.author.name not in info[ctx.guild.name]["admin"]:
        await ctx.send(owo("You do not have the necessary priviledges"))
    else:
        if user.name not in info[ctx.guild.name]["admin"]:
            info[ctx.guild.name]["admin"].append(user.name)
            await ctx.send(owo(f"{user.name} is now admin"))
            store()
        else:
            await ctx.send(owo("User is already admin"))

@admin.command()
async def remove(ctx, *, user: discord.User):
    if ctx.author.name not in info[ctx.guild.name]["admin"]:
        await ctx.send(owo("You do not have the necessary priviledges"))
    else:
        if user.name not in info[ctx.guild.name]["admin"]:
            await ctx.send(owo("User is not admin"))
        else:
            info[ctx.guild.name]["admin"].pop(info[ctx.guild.name]["admin"].index(user.name))
            await ctx.send(owo(f"{user.name} has been removed"))
            store()

@bot.group(name="owo")
async def _owo(ctx):
    if ctx.invoked_subcommand is None:
        with open("log.txt", "a") as log:
            log.write(f"[{time.asctime(time.localtime(time.time()))}] ({ctx.guild.name}/{str(ctx.channel)}/{str(ctx.author)}) {str(ctx.message.content)}\n")
            message = await ctx.channel.fetch_message(last_message[f"{ctx.guild.id}/{ctx.channel.id}"])
            await ctx.send(owo(message.content))
            log.write(f"[{time.asctime(time.localtime(time.time()))}] Complete\n")
        try:
            await ctx.message.delete()
        except:
            pass

@_owo.command()
async def ping(ctx):
    await ctx.send(owo('Pong! {0}'.format(round(bot.latency, 1))))

@_owo.command()
async def help(ctx):
    with open("log.txt", "a") as log:
        log.write(f"[{time.asctime(time.localtime(time.time()))}] ({ctx.guild.name}/{str(ctx.channel)}/{str(ctx.author)}) {str(ctx.message.content)}\n")
        HelpEmbed = discord.Embed(
            title="owoTranslatorBot Command Help",
            type="rich",
            description=helpDescription.format(info[ctx.guild.name]["prefix"])
        )
        await ctx.send(embed=HelpEmbed)
        log.write(f"[{time.asctime(time.localtime(time.time()))}] Complete\n")

@_owo.command()
async def translate(ctx):
    with open("log.txt", "a") as log:
        log.write(f"[{time.asctime(time.localtime(time.time()))}] ({ctx.guild.name}/{str(ctx.channel)}/{str(ctx.author)}) {str(ctx.message.content)}")
        message = await ctx.channel.fetch_message(last_message[f"{ctx.guild.id}/{ctx.channel.id}"])
        await ctx.send(owo(message.content, translate=True))
        log.write(f"[{time.asctime(time.localtime(time.time()))}] Complete\n")
    try:
        await ctx.message.delete()
    except:
        pass

@_owo.command()
async def reverse(ctx):
    with open("log.txt", "a") as log:
        log.write(f"[{time.asctime(time.localtime(time.time()))}] ({ctx.guild.name}/{str(ctx.channel)}/{str(ctx.author)}) {str(ctx.message.content)}\n")
        message = await ctx.channel.fetch_message(last_message[f"{ctx.guild.id}/{ctx.channel.id}"])
        await ctx.send(owo(message.content, reverse=True))
        log.write(f"[{time.asctime(time.localtime(time.time()))}] Complete\n")
    try:
        await ctx.message.delete()
    except:
        pass


bot.run("TOKEN")
