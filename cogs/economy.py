import json
import discord
from discord.ext import commands

main_colour = 0xb3701e
async def getBankData():
  with open('cogs/json/bank.json','r') as f:
    data=json.load(f) 
    return data



async def openAccount(user:discord.Member):
  data= await getBankData()
  if not str(user.id) in data:
    data[str(user.id)]={}
    data[str(user.id)]["wallet"]=0
    data[str(user.id)]["bank"]=0
    with open('cogs/json/bank.json','w') as f:
      json.dump(data, f)

class Economy(commands.Cog):
  def __init__(self, client):
    self.client=client

  @commands.Cog.listener()
  async def on_ready(self):
    print(f"{self.qualified_name} is ready")

  @commands.command(name='deposit', aliases=['dep'])
  async def add(self,ctx, amount:int):
    data = await getBankData()
    if amount<0:
      await ctx.send("Needs to be greater than 0")
    elif amount==0:
      await ctx.send("Needs to be greater than 0")
    elif data[str(ctx.author.id)]["wallet"]<amount:
      await ctx.send("You don't even have that much")
    else:
      
      if not str(ctx.author.id) in data:
        await openAccount(ctx.author)
        await ctx.send("You do not have a bank account. ONe has been opened for you.")
      else:
        data[str(ctx.author.id)]["bank"]+=amount
        data[str(ctx.author.id)]["wallet"]-=amount
        with open('cogs/json/bank.json','w') as f:
          json.dump(data,f)
        await ctx.send(f"Deposited {amount} successfully")

  @commands.command(name='withdraw',aliases=['with'])
  async def withdraw(self, ctx, amount:int):
    data=await getBankData()
    if not str(ctx.author.id) in data:
      await openAccount(ctx.author)
    wallet=data[str(ctx.author.id)]["wallet"]
    bank = data[str(ctx.author.id)]["bank"]

  @commands.command(name='balance',aliases=['bal'])
  async def balance(self, ctx, member:discord.Member=None):
    if member==None:
      member=ctx.author
    data=await getBankData()
    if not str(member.id) in data: 
      await openAccount(member)
    else:
      if member.name.startswith("_"):
        name=f"\\{member.name}"
      else:
        name=member.name
      wallet = data[str(member.id)]["wallet"]
      bank = data[str(member.id)]["bank"]
      embed=discord.Embed(title=f"Balance for {name}'s account", description="Here is your bank balance", embed=discord.Color.green())
      embed.add_field(name="Bank balance: ", value=f"{bank}", inline = True)
      embed.add_field(name="wallet balance: ", value=f"{wallet}", inline=True)
      await ctx.send(embed=embed)


def setup(client):
  client.add_cog(Economy(client))


