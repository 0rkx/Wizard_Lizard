import discord
from discord.ext import commands
import json
import random
import asyncio
import datetime


main_colour = 0xb3701e


class error_handaling (commands.Cog):
	def __init__(self,client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.qualified_name} is ready")


	@commands.Cog.listener()
	async def on_command_error(self ,ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			argerroremb = discord.Embed(color = main_colour , title="<:PepeGun:823138344824209442> | Missing Arguements !", description="Hey! You haven't given me all required arguments! How do you expect me to execute the command?")
			await ctx.send(embed=argerroremb)
		if isinstance(error, commands.MissingPermissions):
			permerroremb = discord.Embed(color = main_colour ,title="<:PepeGun:823138344824209442> | Missing Perms!", description="Hey! You don't have the permissions to use this command!")
			await ctx.send(embed=permerroremb)
		if isinstance(error, commands.MemberNotFound):
			memberroremb = discord.Embed(color = main_colour ,title="<:PepeGun:823138344824209442> | Member not found!", description="There ain't no member like that :|")
			await ctx.send(embed=memberroremb)
		if isinstance(error, commands.BotMissingPermissions):
			botpermerror = discord.Embed(color = main_colour ,title=":<:PepeGun:823138344824209442> | Bot Missing Perms!", description="Hey I don't have the permssions to do that :v.")
			await ctx.send(embed=botpermerror)
		if isinstance(error , commands.CommandNotFound):
			nocmderror = discord.Embed(color = main_colour ,title="<:PepeGun:823138344824209442> | Command not found!", description="I don't have a commmand like that mate.")
			await ctx.send(embed=nocmderror)
		if isinstance(error, commands.CommandOnCooldown):
			msg = 'There Is a Cooldown try again in {:.2f}s'.format(error.retry_after)
			await ctx.send(msg)
		if isinstance(error, commands.CommandInvokeError):
			await ctx.send(f"Error running command: `{error}`")
			raise error
		else :
			raise error

def setup(client):
	client.add_cog(error_handaling(client))
