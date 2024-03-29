import os
import discord
import random
import aiohttp
import json

from thispersondoesnotexist import save_picture, get_online_person

from discord.ext import commands
from keepalive import keep_alive

from random_words import RandomWords, RandomNicknames

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

#sets prefix and activity
prefix = "?"
activity = discord.Activity(type=discord.ActivityType.listening,
                            name="the voices in my head")
client = commands.Bot(command_prefix=prefix,
                      case_insensitive=True,
                      intents=intents,
                      help_command=None,
                      activity=activity)

@client.event
#ensures bot is ready
async def on_ready():
    print("I'M READY!!!")
    await client.tree.sync()


@client.hybrid_command(
    description="returns a random integer from a specified range")
#returns a random integer from a specified range
async def number(ctx):
    await ctx.defer()
    try:
        await ctx.send('From? ')

        def check(msg1):
            return msg1.author == ctx.author and msg1.channel == ctx.channel

        msg1 = await client.wait_for("message", check=check)
        await ctx.send('To? ')

        def check(msg2):
            return msg2.author == ctx.author and msg2.channel == ctx.channel

        msg2 = await client.wait_for("message", check=check)
        await ctx.send(
            str(random.randint(int(msg1.content), int(msg2.content))))
    except:
        await ctx.send("Invalid input. Try again.")


@client.hybrid_command(
    description=
    "starts a game in which you guess a random integer from a specified range")
#starts a game in which you guess a random integer from a specified range
async def guess(ctx):
    await ctx.defer()
    try:
        await ctx.send('From? ')

        def check(guess_from):
            return guess_from.author == ctx.author and guess_from.channel == ctx.channel

        guess_from = await client.wait_for("message", check=check)
        await ctx.send('To? ')

        def check(guess_to):
            return (guess_to.author == ctx.author
                    and guess_to).channel == ctx.channel

        guess_to = await client.wait_for("message", check=check)

        computer = random.randint(int(guess_from.content),
                                  int(guess_to.content))
        await ctx.send("Guess my number from " + str(guess_from.content) +
                       " to " + str(guess_to.content))

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        msg = await client.wait_for("message", check=check)

        if int(msg.content) == computer:
            await ctx.send("Correct")
        else:
            await ctx.send(f"Nope it was {computer}")
    except:
        await ctx.send("Invalid input. Try again.")


@client.hybrid_command(
    description=
    "returns a random Discord server member and prompts if you intend to ping the selected member"
)
#returns a random Discord server member and prompts if you intend to ping selected member
async def someone(ctx):
    await ctx.defer()
    users = []
    for member in ctx.guild.members:
        if not member.bot:
            users.append(member)
    await ctx.send("Ping user? (y)/(n)")

    def check(ping):
        return ping.author == ctx.author and ping.channel == ctx.channel

    ping = await client.wait_for("message", check=check)
    if ping.content == "y":
        await ctx.send(random.choice(users).mention)
    elif ping.content == "n":
        await ctx.send(random.choice(users))
    else:
        await ctx.send("Invalid input. Try again.")


@client.hybrid_command(
    description="returns a random outcome from a game of rock paper scissors")
#returns a random outcome from rock, paper, and scissors
async def pix(ctx):
    await ctx.defer()
    result = ["rock :rock:", "paper :roll_of_paper: ", "scissors :scissors:"]
    await ctx.send(random.choice(result))


@client.hybrid_command(
    description="picks a random card from a standard deck of playing cards")
#returns a random card from a standard deck of playing cards
async def card(ctx):
    await ctx.defer()
    card_type = [
        "Ace of ", "2 of ", "3 of ", "4 of ", "5 of ", "6 of ", "7 of ",
        "8 of ", "9 of ", "10 of ", "Jack of ", "Queen of ", "King of "
    ]
    card_suit = ["Spades", "Hearts", "Diamonds", "Clubs"]

    await ctx.send(random.choice(card_type) + random.choice(card_suit))


@client.hybrid_command(description="returns a random word")
#returns a random word from RandomWords API
async def word(ctx):
    await ctx.defer()
    rw = RandomWords()
    await ctx.send(rw.random_word())


@client.hybrid_command(description="returns a random nickname")
#returns a random nickname from RandomNicknames API
async def name(ctx):
    await ctx.defer()
    rn = RandomNicknames()
    await ctx.send(rn.random_nick(gender="u"))


@client.hybrid_command(
    description="loads a random face from thispersondoesnotexist")
#loads a random face from the thispersondoesnotexit API and displays it
async def face(ctx):
    await ctx.defer()
    picture = await get_online_person()
    await save_picture(picture, "grabbedFace.png")
    await ctx.send(file=discord.File(open("grabbedFace.png", "rb")))


@client.hybrid_command(description="generates a random fact")
#returns a random fact from uselessfacts.jsph.pl
async def fact(ctx):
    await ctx.defer()
    url = "https://uselessfacts.jsph.pl/random.json?language=en"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.text()
        data = json.loads(await response.text())
        useless_fact = data["text"]
        await ctx.send(useless_fact)
    except:
        await ctx.send(
            "Cannot connect to fact generation API. Try again later.")


@client.hybrid_command(description="returns a randomized decision")
#returns a randomized decision
async def decision(ctx):
    await ctx.defer()
    decisions = ["Yes.", "No.", "Maybe."]
    await ctx.send(random.choice(decisions))


@client.hybrid_command(description="returns an 8-ball \"advice\"")
#returns an 8-ball "advice"
async def advice(ctx):
    await ctx.defer()
    advices = [
        "It is certain.", "It is decidedly so.", "Without a doubt.",
        "Yes definitely.", "You may rely on it.", "As I see it, yes.",
        "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
        "Reply hazy, try again.", "Ask again later.",
        "Better not tell you now.", "Cannot predict now.",
        "Concentrate and ask again.", "Don't count on it.", "My reply is no.",
        "My sources say no.", "Outlook not so good.", "Very doubtful."
    ]
    await ctx.send(random.choice(advices))
  
@client.hybrid_command(name='help', description='displays bot commands')
async def help(ctx):
    commands = client.walk_commands()
    file = discord.File("thumbnail.png")  
    # Create the embed
    embed = discord.Embed(title="Rando", description="Rando is a simple bot that will help you deal with life's twists and turns. How does it do that?? With randomness, of course!", colour = discord.Color.fuchsia())
    embed.set_footer(text="\"So much of life, it seems to me, is determined by pure randomness.\" -some random guy")
    embed.set_thumbnail(url="attachment://thumbnail.png")
    # Add the commands and their descriptions to the embed
    for command in commands:
        embed.add_field(name=prefix + command.name, value=command.description, inline=False)
    await ctx.send(file=file, embed=embed)

#kills container when the bot gets rate limited
while __name__ == "__main__":
    try:
        keep_alive()
        client.run(os.environ['TOKEN'])
    except:
        os.system("kill 1")
