import datetime
import discord
from discord.ext import commands
import database
import jlc


class JLCCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        await ctx.send("This is a test")

    @commands.command()
    async def list_components(self, ctx):
        with database.Database() as db:
            components = db.get_components()
        message = ""
        for component in components:
            message += component.name
            message += "\n"

        embed = discord.Embed(title="All Current Components")
        embed.timestamp = datetime.datetime.now()
        embed.add_field(name="Components", value=message)
        await ctx.send(embed=embed)

    @commands.command()
    async def add_component(self, *args):
        name = args[0]
        lcsc = args[1]
        channel = args[2]
        with database.Database as db:
            db.add_component(name, lcsc, channel)


    @commands.command()
    async def check(self, ctx: discord.ext.commands.Context):
        await jlc.jlc_stock_routine(ctx.bot)


async def setup(bot):
    await bot.add_cog(JLCCog(bot))
