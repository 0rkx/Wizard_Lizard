import discord
from discord.ext import commands
import json
import os
import random
import asyncio
import datetime
import praw
from PIL import Image , ImageFont , ImageDraw
from io import BytesIO
import requests
import asyncpraw
import aiohttp
import platform
from aiohttp import ClientSession
from prsaw import RandomStuff
from webserver import keep_alive
import statcord

main_colour = 0xb3701e

class EmbedHelpCommand(commands.HelpCommand):

    COLOUR = main_colour 

    def get_ending_note(self):
        return 'Use {0}{1} [command] for more info on a command.'.format(self.clean_prefix, self.invoked_with)

    def get_command_signature(self, command):
        return '{0.qualified_name} {0.signature}'.format(command)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title='Bot Commands', colour=self.COLOUR)
        description = self.context.bot.description
        if description:
            embed.description = description

        for cog, commands in mapping.items():
            name = 'No Category' if cog is None else cog.qualified_name
            filtered = await self.filter_commands(commands, sort=True)
            if filtered:
                value = '\u2002'.join(c.name for c in commands)
                if cog and cog.description:
                    value = '{0}\n{1}'.format(cog.description, value)

                embed.add_field(name=name, value=value)

        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):
        embed = discord.Embed(title='{0.qualified_name} Commands'.format(cog), colour=self.COLOUR)
        if cog.description:
            embed.description = cog.description

        filtered = await self.filter_commands(cog.get_commands(), sort=True)
        for command in filtered:
            embed.add_field(name=self.get_command_signature(command), value=command.short_doc or '...', inline=False)

        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(title=group.qualified_name, colour=self.COLOUR)
        if group.help:
            embed.description = group.help

        if isinstance(group, commands.Group):
            filtered = await self.filter_commands(group.commands, sort=True)
            for command in filtered:
                embed.add_field(name=self.get_command_signature(command), value=command.short_doc or '...', inline=False)

        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)

    send_command_help = send_group_help

def get_prefix(client, message):
    try:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
            return prefixes[str(message.guild.id)]
        
    except KeyError: 
        with open('prefixes.json', 'r') as k:
            prefixes = json.load(k)
        prefixes[str(message.guild.id)] = 'w!'

        with open('prefixes.json', 'w') as j:
            json.dump(prefixes, j, indent = 4)

        with open('prefixes.json', 'r') as t:
            prefixes = json.load(t)
            return prefixes[str(message.guild.id)]
        
    except: 
        return 'w!' 

intents = discord.Intents.all()
client = commands.Bot(intents=intents , help_command=EmbedHelpCommand() , command_prefix= (get_prefix))
Color = discord.Colour.random()
key = "7A8Dn3qoGL"
rs = RandomStuff(async_mode=True , api_key = key)
key = "statcord.com-ojBt9AMyayKIyQ6dhCt3"
api = statcord.Client(client ,key)
api.start_loop()

@client.event
async def on_ready():
    print ("Ready")
    await client.change_presence(activity=discord.Game(f"w!help in {len(client.guilds)} servers"))




for filename in os.listdir('./cogs'):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")


@client.event
async def on_guild_join(guild): 
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f) 

    prefixes[str(guild.id)] = 'w!'

    with open('prefixes.json', 'w') as f: 
        json.dump(prefixes, f, indent=4) 

    name = str(guild.name)
    description = str(guild.description)

    owner = str(guild.owner)
    id = str(guild.id)
    region = str(guild.region)
    memberCount = str(guild.member_count)

    icon = str(guild.icon_url)

    embed = discord.Embed(
        title=" Joined a server",
        description=description,
        )
    embed.set_thumbnail(url=icon)
    embed.add_field(name= "Server Name" , value = name , inline = False)
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Server ID", value=id, inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name="Member Count", value=memberCount, inline=True)

    log_channel = client.get_channel(832944803338911765)
    await log_channel.send(embed=embed) 





@client.event
async def on_guild_remove(guild): 
    with open('prefixes.json', 'r') as f: 
        prefixes = json.load(f)

    prefixes.pop(str(guild.id)) 

    with open('prefixes.json', 'w') as f: 
        json.dump(prefixes, f, indent=4)
    

    name = str(guild.name)
    description = str(guild.description)

    owner = str(guild.owner)
    id = str(guild.id)
    region = str(guild.region)
    memberCount = str(guild.member_count)

    icon = str(guild.icon_url)

    embed = discord.Embed(
        title=" Left a Server ",
        description=description,
        )
    embed.set_thumbnail(url=icon)
    embed.add_field(name= "Server Name" , value = name , inline = False)
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Server ID", value=id, inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name="Member Count", value=memberCount, inline=True)

    log_channel = client.get_channel(832944803338911765)
    await log_channel.send(embed=embed) 

@client.event
async def on_message(message):
    if client.user == message.author:
        return

    if message.channel.id == 828552656771350528 :
        async with message.channel.typing():
             response = await rs.get_ai_response(message.content)
             await message.reply(response)

    await client.process_commands(message)

@client.command(pass_context=True)
@commands.has_permissions(administrator=True) 
async def changeprefix(ctx, prefix): 
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f: 
        json.dump(prefixes, f, indent=4)

    await ctx.send(f'Prefix changed to: {prefix}')

@client.command(pass_context=True)
async def meme(ctx):
    
    if not hasattr(client, 'nextMeme'):
        client.nextMeme = getMeme()

    name, url = client.nextMeme
    embed = discord.Embed(title = name)

    embed.set_image(url=url)

    await ctx.send(embed=embed)
    
    client.nextMeme = getMeme()


def getMeme():
    reddit  = praw.Reddit(client_id = "haeimp-lUnhNcw", client_secret = "nZL64R7MdQg8lc0qa3XFtnsnT7zTpQ", username = "0rkx_Bot", password = "Obaid2020", user_agent = "0rxBot")
    subreddit = reddit.subreddit("meme")   
    all_subs = []
    top = subreddit.top(limit=50)

    for submission in top:
        all_subs.append(submission)

    random_sub = random.choice(all_subs)

    name = random_sub.title
    url = random_sub.url

    return name, url


client.remove_command("help")


@client.group()
async def help(ctx):
    embed=discord.Embed(title="Help", url="http://wizardlizard.ml/", description="Help Command", color=0x856319)
    embed.set_author(name=f"{ctx.author}")
    embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/dqyM9Kbbc5kZri2GcBm87GZsNHwP_rJf-7Z4BPlBVd0/%3Fsize%3D1024/https/cdn.discordapp.com/icons/832934847735005224/092ea39443d2ffe13c3a30dedc61c4cb.webp?width=411&height=411")
    embed.add_field(name="Economy", value="All Economy Related Commands", inline=True)
    embed.add_field(name="Configuration", value="Configure the bot", inline=True)
    embed.add_field(name="Moderation", value="Moderate Your Server", inline=True)
    embed.add_field(name="Modules", value="Different Modules", inline=True)
    embed.add_field(name="Information", value="Informative Commands", inline=True)
    embed.add_field(name="Useful", value="Useful Commands", inline=True)
    embed.add_field(name="Fun", value="Commands to have Fun!", inline=True)
    embed.add_field(name="Reddit", value="Reddit Integreation", inline=True)
    embed.set_footer(text=f"use help [command] for more information on a command")
    await ctx.send(embed=embed)

@help.command()
async def Economy(ctx):
    await ctx.send("Module Not Added Yet")

@help.command()
async def configuration(ctx):
    await ctx.send("Module Not Added Yet")
keep_alive()
TOKEN = os.environ['TOKEN']
client.run(TOKEN)