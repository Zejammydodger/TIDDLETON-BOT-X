import json
import discord
from discord.ext import commands
from Tiddleton import RoleChecks, BotDataError, WriteLog

class PoliceCommands(commands.Cog, name="police commands"):
  def __init__(self , bot):
    self.bot = bot
    with open("./BotData/ModuleDat.json", "r") as f:
      try :
        self.data = json.load(f)["Police Commands"]
      except (KeyError, json.JSONDecodeError) as e:
        WriteLog("SYSTEM", f"<{type(e)}> {e}")
        raise BotDataError("Debug JSON")

  async def cog_check(self, ctx):
    return RoleChecks.is_Police(ctx)
    
  @commands.command()
  async def warn(self, ctx, member : discord.Member, *, reason):
    pass

def setup(bot):
    bot.add_cog(PoliceCommands(bot))