import discord
from discord.ext import commands


TOKEN = "ODMyNjkyODU1NzU5MDQ0NjE4.YHnfpw.FsCaJP-xt25hlOr3NqYHgvGaanIr"

class Owner(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, name: str):
        """Load any extension"""
        try:
            self.client.load_extension(f"cogs.{name}")

        except Exception as e:
            return await ctx.send(default.traceback_maker(e))
        await ctx.send(f"✅ | Loaded extension **{name}**")

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, name: str):
        """Unload any extension"""
        try:
            self.client.unload_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(default.traceback_maker(e))
        await ctx.send(f"✅ | Unloaded extension **{name}**")

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, name: str):
        """Reload any loaded extension."""
        try:
            self.client.reload_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(default.traceback_maker(e))
        await ctx.send(f"✅ | Reloaded extension **{name}**")

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send(f"✅ | Shutting down the system ...")
        await self.client.close("ODMyNjkyODU1NzU5MDQ0NjE4.YHnfpw.FsCaJP-xt25hlOr3NqYHgvGaanI")

    @commands.command()
    @commands.is_owner()
    async def restart(self, ctx):
        """Restart the bot"""
        await ctx.send(f"✅ | Restarting down the system ...")
        await self.client.login("ODMyNjkyODU1NzU5MDQ0NjE4.YHnfpw.FsCaJP-xt25hlOr3NqYHgvGaanI")
        await ctx.send(f"Restart Complete")

def setup(client):
    client.add_cog(Owner(client))