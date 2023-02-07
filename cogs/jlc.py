import discord
from discord.ext import commands


class JLCCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        print("xyz")
        await ctx.send("This is a test")


async def setup(bot):
    await bot.add_cog(JLCCog(bot))
