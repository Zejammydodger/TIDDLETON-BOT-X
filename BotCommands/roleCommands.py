import json
import discord
import random
from discord.ext import commands
from Tiddleton import RoleChecks, BotDataError, WriteLog


class RoleCommands(commands.Cog):
	def __init__(self , bot):
		self.bot = bot

	async def cog_check(self, ctx):
		return RoleChecks.is_Admin(ctx)

	@commands.command()
	async def formatRoles(self , ctx : commands.Context , roles : commands.Greedy[discord.Role] , number : int = 1):
		guild = ctx.guild
		names = []
		for mem in guild.members:
			count = 0
			for r in roles:
				if r in mem.roles:
					count += 1
			if count > number:
				for r in roles:
					await mem.remove_roles(r)
				newRoles = random.sample(roles , number)
				for r in newRoles:
					await mem.add_roles(r)
				names.append(mem.display_name)
		newLine = "\n"
		await ctx.send(embed = discord.Embed(title = "roles formatted" , description = f"```{newLine.join(names)}```"))

def setup(bot):
	bot.add_cog(RoleCommands(bot))