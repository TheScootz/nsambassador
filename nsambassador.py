import asyncio
import logging
import os

import discord
import dotenv
import nationstates
import pymongo
from discord.ext import commands

from cogs import verification
from cogs import guildconfig


class NSAmbassador(commands.Bot):
    logger: logging.Logger
    client: pymongo.MongoClient

    def __init__(self, *, intents: discord.Intents):
        super().__init__(command_prefix=[], intents=intents)
        dotenv.load_dotenv()

    async def setup_hook(self):
        self.logger = logging.getLogger(__name__)
        self.client = pymongo.MongoClient(os.environ["MONGO_URL"])
        await self.add_cog(guildconfig.GuildConfig(self))
        await self.add_cog(verification.Verification(self))
    
    async def on_ready(self):
        assert self.user is not None
        self.logger.info(f"Logged in as {self.user} (ID: {self.user.id})")


if __name__ == "__main__":
    intents: discord.Intents = discord.Intents.default()
    bot: discord.Client = NSAmbassador(intents=intents)

    print(f"Running discord.py {discord.__version__}")
    bot.run(os.environ["BOT_TOKEN"], log_level=logging.INFO, root_logger=True)