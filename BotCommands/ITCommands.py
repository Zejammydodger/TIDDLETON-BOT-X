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
    """
    Gets the bots latency and checks if it is online
    """
    await ctx.send(f"Ping : {self.bot.latency}")

  @commands.command()
  async def Log(self, ctx, *, text):
    """
    Writes to the bots debug logging file
    """
    WriteLog(ctx.author.name, text)
    await ctx.send("Successfully logged")

  @commands.command()
  async def ClearLog(self, ctx) :
    """
    Clears the bots debug logging file
    """
    with open("./BotData/Log.txt", "w") as f:
      f.write("")
    await ctx.send("Log Cleared")

  @commands.command()
  async def Load(self, ctx, Ext : str):
    """
    Loads an extension that is not yet loaded
    """
    try:
      self.bot.load_extension(f'BotCommands.{Ext}')
      await ctx.send(embed = discord.Embed(title = "load Sucessful", description=f'BotCommands.{Ext} was Sucessfully loaded', colour=0x00ff00))
    except BaseException as e:
      await ctx.send(embed = discord.Embed(title = "load Failed", description=f'Could not load\n  ```{type(e)} : {e}```', colour=0xff0000))

  @commands.command()
  async def Reload(self, ctx, Ext : str):
    """
    Reloads an extension that is currently loaded
    """
    try:
      self.bot.reload_extension(f'BotCommands.{Ext}')
      await ctx.send(embed = discord.Embed(title = "Reload Sucessful", description=f'BotCommands.{Ext} was Sucessfully reloaded', colour=0x00ff00))
    except BaseException as e:
      await ctx.send(embed = discord.Embed(title = "Reload Failed", description=f'Could not Reload \n  ```{type(e)} : {e}```', colour=0xff0000))
      

def setup(bot):
    bot.add_cog(ITCommands(bot))