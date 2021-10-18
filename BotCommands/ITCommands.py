import json
import discord
from discord.ext import commands
from Tiddleton import RoleChecks, BotDataError, WriteLog

class ITCommands(commands.Cog, name="it commands"):
  def __init__(self , bot):
      self.bot = bot
      with open("./BotData/ModuleDat.json", "r") as f:
        try :
          self.data = json.load(f)["IT Commands"]
        except (KeyError, json.JSONDecodeError) as e:
          WriteLog("SYSTEM", f"<{type(e)}> {e}")
          raise BotDataError("IT Commands JSON")
  
  async def cog_check(self, ctx):
    return RoleChecks.is_IT(ctx)
  
  @commands.command()
  async def Ping(self, ctx):
    await ctx.send(f"Ping : {self.bot.latency}")

  @commands.command()
  async def Log(self, ctx, *, Log):
    WriteLog(ctx.author.name, Log)
    await ctx.send("Successfully logged")

  @commands.command()
  async def ClearLog(self, ctx) :
    with open("./BotData/Log.txt", "w") as f:
      f.write("")
    await ctx.send("Log Cleared")

  @commands.command()
  async def Load(self, ctx, Cog : str):
    try:
      self.bot.load_extension(f'BotCommands.{Cog}')
      await ctx.send(embed = discord.Embed(title = "load Sucessful", description=f'BotCommands.{Cog} was Sucessfully loaded', colour=0x00ff00))
    except BaseException as e:
      await ctx.send(embed = discord.Embed(title = "load Failed", description=f'Could not load\n  ```{type(e)} : {e}```', colour=0xff0000))

  @commands.command()
  async def Reload(self, ctx, Cog : str):
    try:
      self.bot.reload_extension(f'BotCommands.{Cog}')
      await ctx.send(embed = discord.Embed(title = "Reload Sucessful", description=f'BotCommands.{Cog} was Sucessfully reloaded', colour=0x00ff00))
    except BaseException as e:
      await ctx.send(embed = discord.Embed(title = "Reload Failed", description=f'Could not Reload \n  ```{type(e)} : {e}```', colour=0xff0000))
      

def setup(bot):
    bot.add_cog(Debug(bot))