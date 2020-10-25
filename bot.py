import discord, os, time

from Main import owo

client = discord.Client()
prev_message = {}
prefix = {}


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    await client.change_presence(
        activity=discord.CustomActivity("OwO-ing", type="custom"),
        status=discord.Status.online,
    )


@client.event
async def on_message(message):
    if message.guild not in list(prefix):
        prefix[message.guild] = "!"
    if message.author == client.user:
        return
    with open("log.txt", "a") as log:
        try:
            if message.content.startswith(f"{prefix[message.guild]}owo") == False:
                prev_message[f"{message.guild}/{message.channel}"] = message.content

            if message.content.startswith(f"{prefix[message.guild]}owo"):
                log.write(
                    f"[{time.asctime(time.localtime(time.time()))}] ({message.guild}/{message.channel}/{message.author}) {message.content}\n"
                )
                msg = message.content.split(" ")
                if len(msg) > 1:
                    if msg[1].lower() == "prefix":
                        prefix[message.guild] = msg[1].lower()
                        await message.channel.send(
                            owo(
                                f"The prefix has been changed to {prefix[message.guild]}"
                            )
                        )
                        log.write(
                            f"[{time.asctime(time.localtime(time.time()))}] Complete"
                        )

                    if f"{message.guild}/{message.channel}" in list(prev_message):
                        if msg[1].lower() == "translate":
                            await message.channel.send(
                                owo(
                                    prev_message[f"{message.guild}/{message.channel}"],
                                    translate=True,
                                )
                            )
                            log.write(
                                f"[{time.asctime(time.localtime(time.time()))}] Complete\n"
                            )

                        elif msg[1].lower() == "reverse":
                            await message.channel.send(
                                owo(
                                    prev_message[f"{message.guild}/{message.channel}"],
                                    reverse=True,
                                )
                            )
                            log.write(
                                f"[{time.asctime(time.localtime(time.time()))}] Complete\n"
                            )
                    else:
                        await message.channel.send(owo("There is nothing to owo."))

                else:
                    if f"{message.guild}/{message.channel}" in list(prev_message):
                        await message.channel.send(
                            owo(prev_message[f"{message.guild}/{message.channel}"])
                        )
                        log.write(
                            f"[{time.asctime(time.localtime(time.time()))}] Complete\n"
                        )
                    else:
                        await message.channel.send(owo("There is nothing to owo."))
        except Exception as e:
            try:
                await message.channel.send(
                    owo(f"Oops, something has gone wrong ({e})", translate=True)
                )
            except:
                pass
            log.write(f"[{time.asctime(time.localtime(time.time()))}] (error) {e}\n")


client.run("NzY5MjQxNjg4ODExNTAzNjU2.X5MKJg.c3wR82rpu3W9BiWjngCn8L40hh0")
