import discord
from discord.ext import commands
import json
import random
import asyncio
import datetime
from aiohttp import request
import os
from PIL import Image , ImageFont , ImageDraw
from io import BytesIO
from prsaw import RandomStuff

main_colour = 0xb3701e

key = "fnksIUPs8YqW"
rs = RandomStuff(async_mode=True , api_key = key)

q = open("cogs//Text Files//roast.txt","r")
rtopics = q.readlines()

f = open("cogs//Text Files//topic.txt","r")
topics = f.readlines()


class Fun (commands.Cog):
	def __init__(self,client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.qualified_name} is ready")


	@commands.command(help="Used To Make A Wanted Image Of Someone You Mention ")
	async def wanted(self ,ctx, user: discord.Member = None):
		if user == None:
			user = ctx.author

    
		wanted = Image.open("cogs//Images//wanted.png")

		asset = user.avatar_url_as(size = 128)

		data = BytesIO(await asset.read())
		pfp = Image.open(data)
		pfp = pfp.resize((161,161))

		wanted.paste(pfp , (102,168))

		wanted.save("profile.png")

		await ctx.send(file = discord.File("profile.png"))


	@commands.command(help="Used To Generate a Image Of You Beating Someone")
	async def beat(self ,ctx , user : discord.Member = None):
		if user == None:
			await ctx.send("Please Specify A Member to Beat")
			return
		if user == ctx.author:
			await ctx.send("You Cant Beat Yoursef")
			return

		beat = Image.open("cogs//Images//beat.png")


		asset = user.avatar_url_as(size = 128)
		asset1 = ctx.author.avatar_url_as(size = 128)

		data =  BytesIO(await asset.read())

		data1 = BytesIO(await asset1.read())

		pfp = Image.open(data)
		pfp = pfp.resize((158 , 158))
		userpfp = Image.open(data1)
		userpfp = userpfp.resize((127,127))
	     
		beat.paste(pfp , (201,75))
		beat.paste(userpfp , (690,14))

		beat.save("beaten.png")

		await ctx.send(file = discord.File("beaten.png"))

	@commands.command(aliases=["pepe"] , help="Used To Find pp :flushed:")
	async def pp(self , ctx, *, user: discord.Member = None) :
		if user == None:
			user = ctx.author
		dong = "=" * random.randint(1, 15)
		embed= discord.Embed(title=f"{user.display_name}'s pepe size", description=f"8{dong}D", color= main_colour)
		await ctx.send(embed = embed)

	@commands.command(help="Get a random topic to talk on")
	async def topic(self ,ctx):
		random_topic = random.choice(topics)
		await ctx.send(random_topic)

	@commands.command(aliases=['8ball'] , help="When In doubt Ask 8ball")
	async def _8ball(self , ctx, *, question):
			responses = [
				"It is certain.",
				"It is decidedly so.",
				"Without a doubt.",
				"Yes - definitely.",
				"You may rely on it.",
				"As I see it, yes.",
				"Most likely.",
				"Outlook good.",
				"Yes.",
				"Signs point to yes.",
				"Reply hazy, try again.",
				"Ask again later.",
				"Better not tell you now.",
				"Cannot predict now.",
				"Concentrate and ask again.",
				"Don't count on it.",
				"My reply is no.",
				"My sources say no.",
				"Outlook not so good.",
				"Very doubtful."]
			embed = discord.Embed(title="8-ball",description=f"{random.choice(responses)}",color= main_colour)
			await ctx.send(embed=embed)


	@commands.command(help="Get Random Animal Facts")
	@commands.cooldown(1, 40, commands.BucketType.user) 
	async def animal_fact(self, ctx, animal: str):
		if (animal := animal.lower()) in ("dog", "cat", "panda", "fox", "bird", "koala"):
			fact_url = f"https://some-random-api.ml/facts/{animal}"
			image_url = f"https://some-random-api.ml/img/{'birb' if animal == 'bird' else animal}"

			async with request("GET", image_url, headers={}) as response:
				if response.status == 200:
					data = await response.json()
					image_link = data["link"]

				else:
					image_link = None

			async with request("GET", fact_url, headers={}) as response:
				if response.status == 200:
					data = await response.json()

					embed = discord.Embed(title=f"{animal.title()} fact",
								  description=data["fact"],
								  colour= main_colour)
					if image_link is not None:
						embed.set_image(url=image_link)
					await ctx.send(embed=embed)

				else:
					await ctx.send(f"API returned a {response.status} status.")

		else:
			await ctx.send("No facts are available for that animal.")
		




def setup(client):
	client.add_cog(Fun(client))
