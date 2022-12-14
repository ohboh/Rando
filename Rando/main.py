import os
import discord
import random
import requests
import json
from thispersondoesnotexist import save_picture
from thispersondoesnotexist import get_online_person
from discord.ext import commands
from keepalive import keep_alive
from random_words import RandomWords
from random_words import RandomNicknames
intents = discord.Intents.default()
intents.members = True

#changes Discord activity to "Playing you like a fiddle"
prefix = "?"
activity = discord.Game(name="you like a fiddle")
client = commands.Bot(command_prefix=prefix, case_insensitive=True, intents=intents, help_command=None, activity=activity, status=discord.Status.idle)

@client.event
#ensures bot is ready
async def on_ready():
  print("I'M READY!!!")

@client.command()
#returns a random integer from a specified range
async def number(ctx):
  try:
      await ctx.send('From? ')

      def check(msg1):
          return msg1.author == ctx.author and msg1.channel == ctx.channel

      msg1 = await client.wait_for("message", check=check)
      await ctx.send('To? ')

      def check(msg2):
          return msg2.author == ctx.author and msg2.channel == ctx.channel

      msg2 = await client.wait_for("message", check=check)
      await ctx.send(str(random.randint(int(msg1.content), int(msg2.content))))
  except:
    await ctx.send("Invalid input. Try again.")
    
@client.command()
#starts a game in which you guess a random integer from a specified range
async def guess(ctx):
  try:
    await ctx.send('From? ')

    def check(guess_from):
      return guess_from.author == ctx.author and guess_from.channel == ctx.channel

    guess_from = await client.wait_for("message", check=check)
    await ctx.send('To? ')

    def check(guess_to):
      return (guess_to.author == ctx.author and guess_to).channel == ctx.channel

    guess_to = await client.wait_for("message", check=check)

    computer = random.randint(int(guess_from.content), int(guess_to.content))
    await ctx.send("Guess my number from " + str(guess_from.content) + " to " + str(guess_to.content))
  
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await client.wait_for("message", check=check)

    if int(msg.content) == computer:
        await ctx.send("Correct")
    else:
         await ctx.send(f"Nope it was {computer}")
  except:
    await ctx.send("Invalid input. Try again.")
    
@client.command()
#returns a random Discord server member and prompts if you intend to ping selected member
async def someone(ctx):
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

@client.command()
#returns a random outcome from rock, paper, and scissors
async def pix(ctx):
  result = ["rock :rock:", "paper :roll_of_paper: ", "scissors :scissors:"]
  await ctx.send(random.choice(result))

@client.command()
#returns a random card from a standard deck of playing cards
async def card(ctx):
  card_type = ["Ace of ", "2 of ", "3 of ", "4 of ", "5 of ", "6 of ", "7 of ", "8 of ", "9 of ", "10 of ", "Jack of ", "Queen of ", "King of " ]
  card_suit = ["Spades", "Hearts", "Diamonds", "Clubs"]
  
  await ctx.send(random.choice(card_type) + random.choice(card_suit))

@client.command()
#returns a random word from RandomWords API
async def word(ctx):
  rw = RandomWords()
  await ctx.send(rw.random_word())

@client.command()
#returns a random nickname from RandomNicknames API
async def name(ctx):
  rn = RandomNicknames()
  await ctx.send(rn.random_nick(gender="u"))

@client.command()
#loads a random face from the thispersondoesnotexit API and displays it
async def face(ctx):
  picture = await get_online_person()
  await save_picture(picture, "grabbedFace.png")
  await ctx.send(file=discord.File(open("grabbedFace.png", "rb")))
  
@client.command()
#returns a random fact from uselessfacts.jsph.pl
async def fact(ctx):
  url = "https://uselessfacts.jsph.pl/random.json?language=en"
  response = requests.request("GET", url)  
  data = json.loads(response.text)
  useless_fact = data["text"]
  
  await ctx.send(useless_fact)         

@client.command()
#returns a randomized decision
async def decision(ctx):
  decisions = ["Yes.", "No.", "Maybe."]
  await ctx.send(random.choice(decisions))

@client.command()
#returns an 8-ball "advice"
async def advice(ctx):
  advices = ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.", "Reply hazy, try again.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."]
  await ctx.send(random.choice(advices))
  
@client.command()
#displays the bot commands
async def help(ctx):
  await ctx.send("""__**Rando is here!**__\n\nRando is a simple bot that will help you deal with life's twists and turns.\nHow does it do that?? With randomness, of course!\n\n***"So much of life, it seems to me, is determined by pure randomness." -some random guy***\n\n????????????????????????????????????????????????????????????\n**?number:** *returns a random number from a range of numbers you specify.*\n**?word:** *returns a random word.*\n**?name:** *returns a random nickname.*\n**?fact:** *returns a random useless fact.*\n**?face:** *returns a random face from a person that doesn't exist.*\n**?card:** *returns a random card from a standard 52-card deck.*\n**?someone:** *returns a random server member. (can be pinged)*\n**?pix:** :rock: :roll_of_paper: :scissors:\n**?advice + a yes or no question:** *returns random advice. (The bot is not responsible for the repercussions of the decisions you make.)*\n**?guess:** *initiates a game wherein you guess which number the bot is thinking from a range of numbers you specify.*\n\n**+ MORE COMMANDS TO COME IN THE FUTURE!**\n????????????????????????????????????????????????????????????""")

keep_alive()
client.run(os.environ['TOKEN'])