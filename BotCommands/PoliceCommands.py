
import discord
from discord.ext import commands

class PoliceCommands(commands.Cog, name="police commands"):
    def __init__(self , bot):
        self.bot = bot

    @commands.command()
    async def warn(self, ctx, member : discord.Member, *, reason):
      pass

def setup(bot):
    bot.add_cog(PoliceCommands(bot))