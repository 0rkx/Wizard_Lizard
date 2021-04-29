import discord
from discord.ext import commands
import json
import os
import random
import asyncio
import datetime
import requests
import asyncpraw
import aiohttp
import platform
from aiohttp import ClientSession


main_colour = 0xb3701e

class Useful_Commands (commands.Cog):
	def __init__(self,client):
		self.client = client


	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.qualified_name} is ready")

	@commands.command(aliases = ["userinfo"] , help="More Info On The User Mentioned")
	async def whois(self ,ctx, member:discord.Member =  None):

		if member is None:
			member = ctx.author
			roles = [role for role in ctx.author.roles]

		else:
			roles = [role for role in member.roles]

		embed = discord.Embed(title=f"{member}", color = main_colour, timestamp=ctx.message.created_at)
		embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
		embed.set_author(name="User Info: ")
		embed.add_field(name="ID:", value=member.id, inline=False)
		embed.add_field(name="User Name:",value=member.display_name, inline=False)
		embed.add_field(name="Discriminator:",value=member.discriminator, inline=False)
		embed.add_field(name="Current Status:", value=str(member.status).title(), inline=False)
		embed.add_field(name="Current Activity:", value=f"{str(member.activity.type).title().split('.')[1]} {member.activity.name}" if member.activity is not None else "None", inline=False)
		embed.add_field(name="Created At:", value=member.created_at.strftime("%a, %d, %B, %Y, %I, %M, %p UTC"), inline=False)
		embed.add_field(name="Joined At:", value=member.joined_at.strftime("%a, %d, %B, %Y, %I, %M, %p UTC"), inline=False)
		embed.add_field(name=f"Roles [{len(roles)}]", value=" **|** ".join([role.mention for role in roles]), inline=False)
		embed.add_field(name="Top Role:", value=member.top_role, inline=False)
		embed.add_field(name="Bot?:", value=member.bot, inline=False)
		await ctx.send(embed=embed)
		return

	@commands.command(help="Get Covid Sats For The Country Mentioned")
	async def covid( self , ctx, *, countryName = None):
		try:
			if countryName is None:
				embed=discord.Embed(title="This command is used like this: ```!covid [country]```", colour=0xff0000, timestamp=ctx.message.created_at)
				await ctx.send(embed=embed)


			else:
				url = f"https://coronavirus-19-api.herokuapp.com/countries/{countryName}"
				stats = requests.get(url)
				json_stats = stats.json()
				country = json_stats["country"]
				totalCases = json_stats["cases"]
				todayCases = json_stats["todayCases"]
				totalDeaths = json_stats["deaths"]
				todayDeaths = json_stats["todayDeaths"]
				recovered = json_stats["recovered"]
				active = json_stats["active"]
				critical = json_stats["critical"]
				casesPerOneMillion = json_stats["casesPerOneMillion"]
				deathsPerOneMillion = json_stats["deathsPerOneMillion"]
				totalTests = json_stats["totalTests"]
				testsPerOneMillion = json_stats["testsPerOneMillion"]

				embed2 = discord.Embed(title=f"**COVID-19 Status Of {country}**!", description="This Information Isn't Live Always, Hence It May Not Be Accurate!", color = main_colour ,timestamp=ctx.message.created_at)
				embed2.add_field(name="**Total Cases**", value=totalCases, inline=True)
				embed2.add_field(name="**Today Cases**", value=todayCases, inline=True)
				embed2.add_field(name="**Total Deaths**", value=totalDeaths, inline=True)
				embed2.add_field(name="**Today Deaths**", value=todayDeaths, inline=True)
				embed2.add_field(name="**Recovered**", value=recovered, inline=True)
				embed2.add_field(name="**Active**", value=active, inline=True)
				embed2.add_field(name="**Critical**", value=critical, inline=True)
				embed2.add_field(name="**Cases Per One Million**", value=casesPerOneMillion, inline=True)
				embed2.add_field(name="**Deaths Per One Million**", value=deathsPerOneMillion, inline=True)
				embed2.add_field(name="**Total Tests**", value=totalTests, inline=True)
				embed2.add_field(name="**Tests Per One Million**", value=testsPerOneMillion, inline=True)

				embed2.set_thumbnail(url="https://cdn.discordapp.com/attachments/564520348821749766/701422183217365052/2Q.png")
				await ctx.send(embed=embed2)

		except:
			embed3 = discord.Embed(title="Invalid Country Name Or API Error! Try Again..!",color = main_colour , timestamp=ctx.message.created_at)
			embed3.set_author(name="Error!")
			await ctx.send(embed=embed3)


	@commands.command(help="Get The Total Number Of Members In The Server")
	async def members(self ,ctx):

		embed = discord.Embed(title=f"There are {len(ctx.guild.members)} members in {ctx.guild.name}!", color = main_colour , timestamp=ctx.message.created_at)
		embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
		await ctx.send(embed=embed)


	@commands.command(help="Get Info Of the Server At A Glance")
	async def server(self ,ctx):
		name = str(ctx.guild.name)
		description = str(ctx.guild.description)

		owner = str(ctx.guild.owner)
		id = str(ctx.guild.id)
		region = str(ctx.guild.region)
		memberCount = str(ctx.guild.member_count)

		icon = str(ctx.guild.icon_url)

		embed = discord.Embed(
			title=name + " Server Information",
			description=description,
			color = main_colour 
			)
		embed.set_thumbnail(url=icon)
		embed.add_field(name="Owner", value=owner, inline=True)
		embed.add_field(name="Server ID", value=id, inline=True)
		embed.add_field(name="Region", value=region, inline=True)
		embed.add_field(name="Member Count", value=memberCount, inline=True)

		await ctx.send(embed=embed) 

	@commands.command(help="Get The Mentioned Users Profile Picture")
	async def avatar(self ,ctx, *,  avamember : discord.Member=None):
		if avamember == None :
			avamember = ctx.author
		userAvatarUrl = avamember.avatar_url
		await ctx.send(userAvatarUrl)

	@commands.command(aliases=["cs","ci","channelinfo"] , help="Get More Information In The Current Or Mentioned Channel")
	async def channelstats(self ,ctx, channel: discord.TextChannel = None):
			if channel == None:
				channel = ctx.channel

			embed = discord.Embed(title=f"Stats for **{channel.name}**", description=f"{'Category: {}'.format(channel.category.name) if channel.category else 'This channel is not in a category'}", color = main_colour )
			embed.add_field(name="Channel Guild", value=ctx.guild.name, inline=True)
			embed.add_field(name="Channel Id", value=channel.id, inline=True)
			embed.add_field(name="Channel Topic", value=f"{channel.topic if channel.topic else 'No topic'}", inline=False)
			embed.add_field(name="Channel Position", value=channel.position, inline=True)
			embed.add_field(name="Channel Slowmode Delay", value=channel.slowmode_delay, inline=True)
			embed.add_field(name="Channel is nsfw?", value=channel.is_nsfw(), inline=True)
			embed.add_field(name="Channel is news?", value=channel.is_news(), inline=True)
			embed.add_field(name="Channel Permissions Synced",value=channel.permissions_synced,inline=True)
			embed.add_field(name="Channel Hash", value=hash(channel), inline=False)

			await ctx.send(embed=embed)

	@commands.command(aliases=["botsats"] , help="Get More Info On the Discord Bot")
	async def stats(self , ctx):
		pythonVersion = platform.python_version()
		dpyVersion = discord.__version__
		serverCount = len(self.client.guilds)
		memberCount = len(set(self.client.get_all_members()))
		x = 'ALPHA'
		embed = discord.Embed(title=f'{self.client.user.name} Stats', description='\uFEFF', color = main_colour , timestamp=ctx.message.created_at)

		embed.add_field(name='Bot Version:', value= x )
		embed.add_field(name='Python Version:', value=pythonVersion)
		embed.add_field(name='Discord.Py Version', value=dpyVersion)
		embed.add_field(name='Total Guilds:', value=serverCount)
		embed.add_field(name='Total Users:', value=memberCount)
		embed.add_field(name='Bot Developers:', value="<@691278451738411148>")

		embed.set_footer(text=f"Requested By {ctx.author} ")
		embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)

		await ctx.send(embed=embed)


	@commands.command(aliases=["wel"] , help="Used To Welcome Someone")
	async def welcome(self ,ctx):
		async with ctx.channel.typing():
			await ctx.send(f"""
	Hey Welcome To `{str(ctx.guild.name)}` be sure to check out the rules and 
	Have A Fun Time Here!!""")
	

	@commands.command(aliases=["role" , "rs"] , help="Get More Info On The Mentioned Role")
	async def roleinfo(self, ctx, *, role:discord.Role):
		members = f"members: {len(role.members)}" 
		attrs = ["colour", "position", "id", "mentionable"]
		message = "\n".join([f"{attr}: {getattr(role, attr)}" for attr in attrs])

		embed = discord.Embed(title=f"Role info", color = main_colour )
		embed.set_author(name=requested(ctx), icon_url=ctx.author.avatar_url)
		embed.description = f"`\`\`yaml\n---\nname: {role.name}\n{created}\n{members}\n---\n{message}\n---\n`\`\`"
		await ctx.send(embed=embed)


		await ctx.send(embed=em)



	@commands.command(help="Get The Current Ping")
	async def ping(self , ctx):
		 await ctx.send(f'Pong! In {round(self.client.latency * 1000)}ms')




	@commands.command(help = "Get All THe Invite Lniks For A  Bot" )
	async def invite(self, ctx):
		embed = discord.Embed(
					title="All The Necessary Links For The Bot",
					color= main_colour ,
					timestamp=ctx.message.created_at )
		embed.add_field(name = "Invite Wizard Lizard " , value = " Invite Link -- [here](https://discord.com/oauth2/authorize?client_id=832692855759044618&permissions=8&scope=bot%20applications.commands).")
		embed.add_field(name = "Join the support server" , value = " Invite Link -- [here](https://discord.gg/QG8ykbjzMy)" )

		await ctx.send(embed = embed)


	@commands.command()
	async def weather(self , ctx ,location) :

		url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid=7bd9a7e56624005046fc1c9dc58c7763&units=imperial'
		try:
			data = parse_data(json.loads(requests.get(url).content)['main'])
			await ctx.channel.send(embed=weather_message(data, location))
		except KeyError:
			await ctx.channel.send(embed=error_message(location))

color = main_colour
key_features = {
	'temp' : 'Temperature',
	'feels_like' : 'Feels Like',
	'temp_min' : 'Minimum Temperature',
	'temp_max' : 'Maximum Temperature'
}

def parse_data(data):
	del data['humidity']
	del data['pressure']
	return data

def weather_message(data, location):
	location = location.title()
	message = discord.Embed(
		title=f'{location} Weather',
		description=f'Here is the weather in {location}.',
		color=color
	)
	for key in data:
		message.add_field(
			name=key_features[key],
			value=str(data[key]),
			inline=False
		)
	return message

def error_message(location):
	location = location.title()
	return discord.Embed(
	title='Error',
        description=f'There was an error retrieving weather data for {location}.',
        color=color
    )



def setup(client):
	client.add_cog(Useful_Commands(client))