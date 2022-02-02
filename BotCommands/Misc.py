import discord
from discord.ext import commands

import json
import typing
import asyncio as asy

from Tiddleton import RoleChecks, BotDataError, WriteLog

class Misc(commands.Cog, name="miscellaneous"):
  def __init__(self, bot):
    self.bot = bot
    with open("./BotData/ModuleDat.json", "r") as f:
      try :
        self.data = json.load(f)["Misc"]
      except (KeyError, json.JSONDecodeError) as e:
        WriteLog("SYSTEM", f"<{type(e)}> {e}")
        raise BotDataError("Debug JSON")

  @commands.command()
  async def Test(self, ctx, role : discord.Role) :
    await ctx.send(f"{len(role.members)}")

  @commands.command()
  async def CreateTeam(self, ctx, name, color, role : discord.Role): 
    """
    Creates a team
    """
    try :
      self.data["teams"]
    except KeyError:
      self.data["teams"] = dict()

    self.data["teams"][name] = (name, color, 0, role.id) # name color scores

    with open("./BotData/ModuleDat.json", "r") as f:
      db = json.load(f)
      db["Misc"] = self.data
      print(db)
  
    with open("./BotData/ModuleDat.json", "w") as f:
      f.write(json.dumps(db, indent=4))
      print(json.dumps(db,indent=4))

    await ctx.send(
      embed=discord.Embed(
        title="Created ✔️",
        description="Successfully created team",
        color=0x00ff00
      )
    )
      
  @commands.command()
  async def UpdateScores(self, ctx, team, amount : int):
    """
    Updates the team scores
    """
    self.data["teams"][team][2] += amount
    await ctx.send(
      embed=discord.Embed(
      title=f"Scores Updated for {team}",
      description=f"New Score : {self.data['teams'][team][2]}",
      color=0x00ff00
      )
    )

  @commands.command()
  async def TeamScores(self, ctx):
    """
    Gets the current scores
    """
    for team in self.data["teams"].values() :

      r = ctx.guild.get_role(team[3])

      await ctx.send(
        embed=discord.Embed(
          title=team[0],
          description=f"points : {team[2]}\nmembers : {len(r.members)}\ntotal : {team[2] + len(r.members)}",
          color=int(team[1], base=16)
        )
      )

def setup(bot):
    bot.add_cog(Misc(bot))