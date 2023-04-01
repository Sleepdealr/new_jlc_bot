import discord
from discord.ext import commands
from datetime import datetime


class UsersCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def echo(self, ctx: discord.ext.commands.Context, args):
        await ctx.send(content=args)

    @commands.command()
    async def iam(self, ctx: discord.ext.commands.Context, *args):
        role = discord.utils.get(ctx.guild.roles, name=args[0])
        if role:
            await ctx.author.add_roles(role)
            await ctx.message.add_reaction("👍")
        else:
            await ctx.message.add_reaction("👎")

    @commands.command()
    async def iam(self, ctx: discord.ext.commands.Context, *args):
        role = discord.utils.get(ctx.guild.roles, name=args[0])
        if role:
            await ctx.author.remove_roles(role)
            await ctx.message.add_reaction("👍")
        else:
            await ctx.message.add_reaction("👎")

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx: discord.ext.commands.Context):
        await ctx.bot.close()

    @commands.command()
    async def uptime(self, ctx):
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        await ctx.send(f"{days}d, {hours}h, {minutes}m, {seconds}s")


async def setup(bot):
    await bot.add_cog(UsersCog(bot))
