#### loads commands ####
#just some fun stuff to add to the bot 
from discord.ext import commands

class Simple(commands.Cog):
    def __init__(self , bot):
        self.bot = bot

    @commands.command()
    async def Ping(self, ctx):
      await ctx.send("Pong")

def setup(bot):
    bot.add_cog(Simple(bot))




