import datetime
import discord
from discord.ext import tasks, commands
import database
import jlc

# 10am EST to UTC
utc = datetime.timezone.utc
time = datetime.time(hour=15, tzinfo=utc)


class JLCCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_jlc.start()

    @commands.command()
    async def test(self, ctx):
        await ctx.send("This is a test")

    @commands.command()
    async def list_components(self, ctx):
        components = await database.get_components(ctx)
        message = ""
        for component in components:
            message += component.name
            message += "\n"

        embed = discord.Embed(title="All Current Components")
        embed.timestamp = datetime.datetime.now()
        embed.add_field(name="Components", value=message)
        await ctx.send(embed=embed)

    @commands.command()
    async def add_component(self, ctx, *args):
        name = args[0]
        lcsc = args[1]
        channel = args[2]
        await database.add_component(ctx.bot, name, lcsc, channel)

    @commands.command()
    async def check(self, ctx: discord.ext.commands.Context):
        await jlc.jlc_stock_routine(self.bot)

    @tasks.loop(time=time)
    async def check_jlc(self):
        # Background task, call daily discord check from here
        await jlc.jlc_stock_routine(self.bot)


async def setup(bot: discord.ext.commands.Bot):
    await bot.add_cog(JLCCog(bot))
