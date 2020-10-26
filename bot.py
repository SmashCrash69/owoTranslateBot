import discord, time

from Translator import owo

client = discord.Client()
prev_message = {}
prefix = {}


def prefixLog(prefix):
    keys = []
    with open("prefixes.txt", "a+") as file:
        for line in file:
            line = line.split(":")
            keys.append(line[0])
        for k in prefix:
            if k in keys:
                pass
            else:
                file.write(f"{k}:{prefix[k]}")


def prefixCollect():
    with open("prefixes.txt", "w+") as file:
        if file.read() != "":
            for line in file:
                line = line.split(":")
                prefix[line[0]] = line[1]
        else:
            return


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    await client.change_presence(
        activity=discord.CustomActivity("OwO-ing", type="custom"),
        status=discord.Status.online,
    )
    prefixCollect()


@client.event
async def on_message(message):
    with open("log.txt", "a") as log:
        if message.guild.name != "None":
            if message.guild.name not in list(prefix):
                prefix[message.guild.name] = "!"
                log.write(
                    f"[{time.asctime(time.localtime(time.time()))}] ({message.guild.name}) server added\n"
                )
                prefixLog(prefix)
        if message.author == client.user:
            return
        try:
            if message.content.startswith(f"{prefix[message.guild.name]}owo") == False:
                prev_message[f"{message.guild}/{message.channel}"] = message.content
                return

            if message.content.startswith(f"{prefix[message.guild.name]}owo"):
                log.write(
                    f"[{time.asctime(time.localtime(time.time()))}] ({message.guild.name}/{str(message.channel)}/{str(message.author)}) {str(message.content)}\n"
                )
                msg = message.content.split(" ")
                if len(msg) > 1:
                    if msg[1].lower() == "prefix":
                        print(message.guild.name)
                        prefix[message.guild.name] = msg[2].lower()
                        await message.channel.send(
                            owo(
                                f"The prefix has been changed to {prefix[message.guild.name]}"
                            )
                        )
                        log.write(
                            f"[{time.asctime(time.localtime(time.time()))}] Complete"
                        )
                        prefixLog(prefix)
                        return

                    if f"{message.guild.name}/{message.channel}" in list(prev_message):
                        if msg[1].lower() == "translate":
                            await message.channel.send(
                                owo(
                                    prev_message[
                                        f"{message.guild.name}/{message.channel}"
                                    ],
                                    translate=True,
                                )
                            )
                            log.write(
                                f"[{time.asctime(time.localtime(time.time()))}] Complete\n"
                            )
                            return

                        elif msg[1].lower() == "reverse":
                            await message.channel.send(
                                owo(
                                    prev_message[
                                        f"{message.guild.name}/{message.channel}"
                                    ],
                                    reverse=True,
                                )
                            )
                            log.write(
                                f"[{time.asctime(time.localtime(time.time()))}] Complete\n"
                            )
                            return
                    else:
                        await message.channel.send(owo("There is nothing to owo."))
                        return

                else:
                    if f"{message.guild}/{message.channel}" in list(prev_message):
                        await message.channel.send(
                            owo(prev_message[f"{message.guild}/{message.channel}"])
                        )
                        log.write(
                            f"[{time.asctime(time.localtime(time.time()))}] Complete\n"
                        )
                        return
                    else:
                        await message.channel.send(owo("There is nothing to owo."))
                        return
        except Exception as e:
            try:
                await message.channel.send(
                    owo(f"Oops, something has gone wrong ({e})", translate=True)
                )
            except:
                pass
            log.write(f"[{time.asctime(time.localtime(time.time()))}] (error) {e}\n")
            return


client.run("NzY5MjQxNjg4ODExNTAzNjU2.X5MKJg.0rqGKPrcXR6AYMvYW1dBxN84hSQ")

