import configparser
import discord
from discord.ext import tasks, commands
import datetime
import jlc

CONFIG = configparser.ConfigParser()
CONFIG.read("jlc.conf")

# 10am EST to UTC
utc = datetime.timezone.utc
time = datetime.time(hour=15, tzinfo=utc)


class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=CONFIG["discord"]["prefix"], intents=intents)
        self.initial_extensions = [
            'cogs.jlc',
            'cogs.users'
        ]

    async def setup_hook(self):
        self.check_jlc.start()
        for ext in self.initial_extensions:
            await self.load_extension(ext)

    async def close(self):
        await super().close()

    @tasks.loop(time=time)
    async def check_jlc(self):
        # Background task, call daily discord check from here
        await jlc.jlc_stock_routine(bot)

    async def on_ready(self):
        print('Ready!')


bot = MyBot()
# check_jlc.start()
bot.run(CONFIG["discord"]["token"])
