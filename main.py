##### the one that runs! ####
import discord
from discord.ext import commands
import os

from Keep_Alive import keep_alive
import random as r
from inspect import Parameter

intents = discord.Intents(messages=True, guilds=True, members=True)

bot = commands.Bot(command_prefix="X!", case_insensitive = True, intents = intents)

bot.remove_command("help")

for Command in filter(lambda x: ".py" in x, os.listdir("./BotCommands/")): # 
	try:
		bot.load_extension(f"BotCommands.{Command[:-3]}")
		print(f"Loaded : BotCommands.{Command[:-3]}")
	except BaseException as e:
		print(f"Failed to load BotCommands.{Command[:-3]} because {e}")

@bot.event
async def on_ready(bot):
  print("Ready")
bot.run(os.environ.get("TOKEN"))