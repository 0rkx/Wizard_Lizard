import discord
from discord.ext import commands
import random
import asyncio
import datetime
import praw
import requests
import asyncpraw
import aiohttp
from aiohttp import ClientSession

main_colour = 0xb3701e


class reddit (commands.Cog):
	def __init__(self,client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.qualified_name} is ready")


	@commands.command(help="Get A Random Fact From Reddit!")
	@commands.cooldown(1, 40, commands.BucketType.user)   
	async def fact(self,ctx):
			async with ctx.channel.typing():
				reddit  = asyncpraw.Reddit(client_id = "haeimp-lUnhNcw", client_secret = "nZL64R7MdQg8lc0qa3XFtnsnT7zTpQ", username = "0rkx_Bot", password = "Obaid2020", user_agent = "0rxBot")
				subreddit = await  reddit.subreddit("fact")

				all_subs = []
			
				async for submission in subreddit.hot(limit=30):
					all_subs.append(submission)
					random_sub = random.choice(all_subs)
					name = random_sub.title
					url = random_sub.url
					score = random_sub.score

	          
			embed = discord.Embed(
				description =  f"**[{name}]({url})**",

				color =  0xb3701e
				)
	    
			embed.set_author(name=f"Requested by {ctx.author}", icon_url= ctx.author.avatar_url)
			embed.set_image(url=url)
			embed.set_footer(text=f"👍 {score}")

			await ctx.send(embed=embed)

	@commands.command(help="Get A Random Anime Meme From Reddit!")
	@commands.cooldown(1, 40, commands.BucketType.user)   
	async def ameme(self,ctx):
			async with ctx.channel.typing():
				reddit  = asyncpraw.Reddit(client_id = "haeimp-lUnhNcw", client_secret = "nZL64R7MdQg8lc0qa3XFtnsnT7zTpQ", username = "0rkx_Bot", password = "Obaid2020", user_agent = "0rxBot")
				subreddit = await  reddit.subreddit("Animemes")

				all_subs = []
			
				async for submission in subreddit.hot(limit=30):
					all_subs.append(submission)
					random_sub = random.choice(all_subs)
					name = random_sub.title
					url = random_sub.url
					score = random_sub.score

	          
			embed = discord.Embed(
				description =  f"**[{name}]({url})**",

				color =  main_colour
			)

	    
			embed.set_author(name=f"Requested by {ctx.author}", icon_url= ctx.author.avatar_url)
			embed.set_image(url=url)
			embed.set_footer(text=f"👍 {score}")

			await ctx.send(embed=embed)





	@commands.command(help="Get A Random Tifu Post From Reddit!")
	@commands.cooldown(1, 40, commands.BucketType.user)   
	async def tifu( self , ctx):
		async with ctx.channel.typing():
			reddit  = asyncpraw.Reddit(client_id = "haeimp-lUnhNcw", client_secret = "nZL64R7MdQg8lc0qa3XFtnsnT7zTpQ", username = "0rkx_Bot", password = "Obaid2020", user_agent = "0rxBot")
			subreddit = await  reddit.subreddit("tifu")

			all_subs = []
	          
			async for submission in subreddit.hot(limit=30):
					all_subs.append(submission)
					random_sub = random.choice(all_subs)
					name = random_sub.title
					url = random_sub.url
					score = random_sub.score
					content = random_sub.selftext

	              
			embed = discord.Embed(
				title = f"**[{name}]({url})**" ,
				description = f"{content}",

				color = main_colour


			)

	        
			embed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
			embed.set_image(url=url)
			embed.set_footer(text=f"👍 {score}")

			await ctx.send(embed=embed)


	@commands.command(help="Get A Random Post From r/teenagers")
	@commands.cooldown(1, 40, commands.BucketType.user)   
	async def teen( self , ctx):
		async with ctx.channel.typing():
			reddit  = asyncpraw.Reddit(client_id = "haeimp-lUnhNcw", client_secret = "nZL64R7MdQg8lc0qa3XFtnsnT7zTpQ", username = "0rkx_Bot", password = "Obaid2020", user_agent = "0rxBot")
			subreddit = await  reddit.subreddit("teenagers")

			all_subs = []
	          
			async for submission in subreddit.hot(limit=30):
					all_subs.append(submission)
					random_sub = random.choice(all_subs)
					name = random_sub.title
					url = random_sub.url
					score = random_sub.score
					content = random_sub.selftext

	              
			embed = discord.Embed(
				title = f"**[{name}]({url})**" ,
				description = f"{content}",

				color = main_colour


			)

	        
			embed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
			embed.set_image(url=url)
			embed.set_footer(text=f"👍 {score}")

			await ctx.send(embed=embed)

	@commands.command(help="Get A Random showerthought")
	@commands.cooldown(1, 40, commands.BucketType.user)  
	async def showerthought(self,ctx):
			async with ctx.channel.typing():
				reddit  = asyncpraw.Reddit(client_id = "haeimp-lUnhNcw", client_secret = "nZL64R7MdQg8lc0qa3XFtnsnT7zTpQ", username = "0rkx_Bot", password = "Obaid2020", user_agent = "0rxBot")
				subreddit = await  reddit.subreddit("showerthoughts")

				all_subs = []
			
				async for submission in subreddit.hot(limit=30):
					all_subs.append(submission)
					random_sub = random.choice(all_subs)
					name = random_sub.title
					url = random_sub.url
					score = random_sub.score

	          
			embed = discord.Embed(
				description =  f"**[{name}]({url})**",

				color = main_colour
				)

	    
			embed.set_author(name=f"Requested by {ctx.author}", icon_url= ctx.author.avatar_url)
			embed.set_image(url=url)
			embed.set_footer(text=f"👍 {score}")

			await ctx.send(embed=embed)

	@commands.command(help="Get A Random Cat Image")
	async def cat(self ,ctx):
            async with ctx.channel.typing():
                async with aiohttp.ClientSession() as cs:
                    async with cs.get('http://aws.random.cat/meow') as r:
                        data = await r.json()

                        em = discord.Embed(title='Cat',timestamp=ctx.message.created_at , color = main_colour)
                        em.set_image(url = data['file'])
                        em.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested By {ctx.author.name}")
                        await ctx.send(embed=em)

	@commands.command(help="Get A Random DadJoke")
	async def dadjoke(self ,ctx):
		url = "https://dad-jokes.p.rapidapi.com/random/jokes"

		headers = {
		    "x-rapidapi-key": "07c568cf37mshb26ee618251f676p1dd6fbjsncf14e54f989a",
		"x-rapidapi-host": "dad-jokes.p.rapidapi.com" 
		}
	    

		async with ClientSession() as session:
			async with session.get(url, headers=headers) as response:
				r = await response.json()
				r = r["body"][0]
				await ctx.send(f"**{r['setup']}**\n\n||{r['punchline']}||")
 
	

def setup(client):
	client.add_cog(reddit(client))