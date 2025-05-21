import asyncio
import logging
import os

import discord
import dotenv
import nationstates
import pymongo
from discord.ext import commands

from cogs import verification


class NSAmbassador(commands.Bot):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(command_prefix=[], intents=intents)
        dotenv.load_dotenv()

    async def setup_hook(self):
        self.db = pymongo.MongoClient(os.environ["MONGO_URL"])[os.environ["MONGO_DB"]]
        await self.add_cog(verification.Verification(self))
    
    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
    
    async def on_guild_available(self, guild):
        # Synchronize commands with servers
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)


if __name__ == "__main__":
    intents = discord.Intents.default()
    bot = NSAmbassador(intents=intents)

    print(f"Running discord.py {discord.__version__}")
    bot.run(os.environ["BOT_TOKEN"], log_level=os.getenv("LOG_LEVEL", logging.NOTSET))