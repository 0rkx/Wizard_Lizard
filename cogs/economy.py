import json
import discord
from discord.ext import commands


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

  @commands.command(name='add')
  async def add(self,ctx, amount:int):
    if amount<0:
      pass
    else:
      await openAccount(ctx.author)
      data=await getBankData()
      data[str(ctx.author.id)]["wallet"]+=amount
      with open('cogs/json/bank.json','w') as f:
        json.dump(data, f)

def setup(client):
  client.add_cog(Economy(client))


