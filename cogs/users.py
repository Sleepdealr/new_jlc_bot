import discord
from discord.ext import commands


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


async def setup(bot):
    await bot.add_cog(UsersCog(bot))
