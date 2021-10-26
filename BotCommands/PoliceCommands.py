import json
import discord
from discord.ext import commands
import typing
import asyncio as asy
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
    """
    NYI
    """
    pass

  @commands.command()
  @commands.has_permissions(manage_channels = True)
  async def SlowMode(self, ctx, Delay : typing.Optional[int] = 5, Channels : commands.Greedy[discord.TextChannel] = None, Time : typing.Optional[int] = None, *, reason = ''):
    """
    Sets slow mode for the tagged/current channel(s)
    """
    if not(Channels) : Channels = [ctx.channel]
    for Channel in Channels:
      Channel.slowmode_delay = Delay
      await Channel.send(embed = discord.Embed(title = "SLOWMODE ENABLED", description = f'a Slow Mode of {Delay} seconds has been enabled by admin {ctx.author.mention} ' +
      f'due to {reason}. ' * (len(reason) != 0) +
      f'and will be unlocked in {Time} seconds. ' * (Time != None) + 'if you feel like this admin has made a mistake and/or this slowmode was unjustified please raise this issue with another member of staff', color = 0x7a6b32))
    if Time:
      await asy.sleep(Time)
      for Channel in Channels:
        Channel.slowmode_delay = 0

def setup(bot):
    bot.add_cog(PoliceCommands(bot))