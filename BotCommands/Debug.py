from discord.ext import commands
import datetime
import json

class Debug(commands.Cog, name="debug"):
    def __init__(self , bot):
        self.bot = bot
        with open("ModuleDat.json", "r") as f:
          try :
            self.data = json.load(f)["Debug"]
          except (KeyError, json.JSONDecodeError):
            self.data = {}

    @commands.command()
    async def Ping(self, ctx):
      await ctx.send(f"Ping : {self.bot.latency}")

    @commands.command()
    async def Log(self, ctx, *, Log):
      with open("Log.txt", "a") as f:
        now = datetime.datetime.now().strftime("[%d/%H/%y %T]")
        f.write(f"{now}>> {ctx.author.name} : {Log}\n")
      await ctx.send("Successfully logged")

    @commands.command()
    async def ClearLog(self, ctx) :
      with open("Log.txt", "w") as f:
        f.write("")
      await ctx.send("Log Cleared")
      

def setup(bot):
    bot.add_cog(Debug(bot))