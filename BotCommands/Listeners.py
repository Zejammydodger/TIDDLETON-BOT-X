import discord
from discord.ext import commands

import json
import typing
import asyncio as asy

from Tiddleton import RoleChecks, BotDataError, WriteLog

class <name>(commands.Cog, name="<display>"):
  def __init__(self, bot):
    self.bot = bot
    with open("./BotData/ModuleDat.json", "r") as f:
      try :
        self.data = json.load(f)["<name>"]
      except (KeyError, json.JSONDecodeError) as e:
        WriteLog("SYSTEM", f"<{type(e)}> {e}")
        raise BotDataError("Debug JSON")

  @commands.command()
  async def Example(self, ctx):
    """
    DESCRIPTION
    """
    pass

def setup(bot):
    bot.add_cog(<name>(bot))