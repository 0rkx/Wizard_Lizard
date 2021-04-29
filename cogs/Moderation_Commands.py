import discord
from discord.ext import commands
import random
import asyncio
import datetime
import requests
import aiohttp
from aiohttp import ClientSession

main_colour = 0xb3701e

class moderation (commands.Cog):
	def __init__(self,client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.qualified_name} is ready")

	@commands.command( help="Used To Conduct A Poll With 👍 and 👎 as options ")
	@commands.has_permissions(kick_members = True)
	async def poll(self , ctx,*,message):
		emb=discord.Embed(title="POLL", description=f"{message}" , color = main_colour )
		msg=await ctx.channel.send(embed=emb)
	
		await msg.add_reaction('👍')
		await msg.add_reaction('👎')

	@commands.command(aliases=['sslowmode','slowmode'], help="Used To Set Slomode Of The Current Channel")
	@commands.has_permissions(kick_members=True)
	async def setslowmode(self ,ctx,tm):
		t = convert_time_to_seconds(tm)
		await ctx.channel.edit(slowmode_delay=t)

		if tm.find('h')!=-1 or tm.find('s')!=-1 or tm.find('m')!=-1:
			await ctx.send(f"⌚ Set the slowmode delay in this channel to {tm}!")
			return False
		else:
			await ctx.send(f"⌚ Set the slowmode delay in this channel to {tm}s!")



	def convert_time_to_seconds(time):
		time_convert = {"s": 1, "m": 60, "h": 3600}

		try:
			return int(time[:-1]) * time_convert[time[-1]]
		except:
			return time


	@commands.command(help="Used To Conduct A Poll with 1️⃣' and  2️⃣' as options")
	@commands.has_permissions(kick_members = True)
	async def poll1(self , ctx,*,message):
		emb=discord.Embed(color = main_colour ,title="POLL", description=f"{message}")
		msg=await ctx.channel.send(embed=emb)
	    
		await msg.add_reaction('1️⃣')
		await msg.add_reaction('😑')
		await msg.add_reaction('2️⃣')

	@commands.command(help="Used To Lock The Current Channel")
	@commands.has_permissions(manage_channels=True)
	async def lock(self ,ctx, channel : discord.TextChannel=None):
		channel = channel or ctx.channel
		overwrite = channel.overwrites_for(ctx.guild.default_role)
		overwrite.send_messages = False
		await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
		embed = discord.Embed(title = '' , description = f' Locked the Channel {channel.mention}' , color = discord.Color.red())
		await ctx.send(embed=embed)

	@commands.command(help="Used To Unlock A Channel")
	@commands.has_permissions(manage_channels=True)
	async def unlock(self ,ctx, channel : discord.TextChannel=None):
		channel = channel or ctx.channel
		overwrite = channel.overwrites_for(ctx.guild.default_role)
		overwrite.send_messages = True
		await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
		embed = discord.Embed(title = '' , description = f' Unlocked the Channel {channel.mention}' , color = discord.Color.green())
		await ctx.send(embed=embed)

	@commands.command(help="Used To Check All The Banned Members In The Server")
	@commands.has_permissions(ban_members=True)
	async def bans(self ,ctx) :
    
		users = await ctx.guild.bans()
		if len(users) > 0 :
			msg = f'`{"ID":21}{"Name":25} Reason\n'
			for entry in users :
				userID = entry.user.id
				userName = str(entry.user)
				if entry.user.bot :
					username = '🤖' + userName 
				reason = str(entry.reason) 
				msg += f'{userID:<21}{userName:25} {reason}\n'
			embed = discord.Embed(color = main_colour)  
			embed.set_thumbnail(url=ctx.guild.icon_url)
			embed.set_footer(text=f'Server: {ctx.guild.name}')
			embed.add_field(name='Ranks', value=msg + '`', inline=True)
			await ctx.send(embed=embed)
		else :
			await ctx.send('**:negative_squared_cross_mark:** There arent banned people!')



def convert_time_to_seconds(time):
		time_convert = {"s": 1, "m": 60, "h": 3600}

		try:
			return int(time[:-1]) * time_convert[time[-1]]
		except:
			return time


def setup(client):
	client.add_cog(moderation(client))