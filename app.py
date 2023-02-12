import configparser
import asyncpg
import discord
from discord.ext import commands

CONFIG = configparser.ConfigParser()
CONFIG.read("jlc.conf")


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
        for ext in self.initial_extensions:
            await self.load_extension(ext)
        bot.pool = await asyncpg.create_pool(CONFIG["postgres"]["database_url"])

    async def close(self):
        await super().close()

    async def on_ready(self):
        print('Ready!')


bot = MyBot()
bot.run(CONFIG["discord"]["token"])
exit(1) # Only triggered after logout
