##### the one that runs! ####
import os

import discord
from discord.ext import commands
from discord.utils import get

from Keep_Alive import keep_alive
from inspect import Parameter
from Tiddleton import RoleIDs

intents = discord.Intents(messages=True, guilds=True, members=True)
  
def GetPrefix(a, b):
	return "&"

bot = commands.Bot(command_prefix=GetPrefix, case_insensitive = True, intents = intents)

bot.remove_command("help")

for Command in filter(lambda x: ".py" in x, os.listdir("./BotCommands/")): # 
	try:
		bot.load_extension(f"BotCommands.{Command[:-3]}")
		print(f"Loaded : BotCommands.{Command[:-3]}")
	except BaseException as e:
		print(f"Failed to load BotCommands.{Command[:-3]} because {e}")

@bot.event
async def on_ready():
  print("Ready")

def CommandInfo(com, bot, ctx):
  Args = [('<' * (Ty.default != Parameter.empty) or '[')+ f'{Key}' + (':Optional>' * (Ty.default != Parameter.empty) or ']')for Key, Ty in com.clean_params.items()]
  return f'''`{GetPrefix(bot, ctx)[0]}{com.name} {' '.join(Args)}`\n{com.help}'''

@bot.command()
async def HelpNew(ctx, *, option = None):
  with open("./BotData/HelpIgnore.txt","r") as f:
    Locked = f.read().split('\n')

  Ignore = []
  for i, Category in enumerate(Locked) :
    cog, name = Category.split(':')
    ID = RoleIDs.IDTable[name]

    if not get(ctx.guild.roles, id=ID) in ctx.author.roles :
      Ignore.append(cog)


  cogList = list(filter(lambda x : not bot.get_cog(x).qualified_name in Ignore, bot.cogs))

  if option :
    cog = bot.get_cog(option.lower())
    if cog and (option in cogList):
      CogCommands = cog.get_commands()
      emb = discord.Embed(title = cog.qualified_name, description = '\n\n'.join([CommandInfo(command,bot, ctx) for command in CogCommands])+ "**N/A**" * (len(CogCommands) == 0), color = 0x884c9e)
    else:
      emb = discord.Embed(title = "ERROR 404 NOT FOUND", color = 0x884c9e)

  else :
    emb = discord.Embed(title = "Tiddleton Bot Categories", color = 0x884c9e)
    for cog in cogList:
      emb.add_field(name = cog, value = f"`{GetPrefix(bot, ctx)[0]}Help {cog}`")

  emb.set_thumbnail(url=bot.user.avatar_url)
  await ctx.send(embed = emb)

keep_alive()
bot.run(os.environ.get("TOKEN"))