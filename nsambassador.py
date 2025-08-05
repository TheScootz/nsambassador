import asyncio
import logging
import os

import discord
import nationstates
import pymongo
from discord.ext import commands

import config
from cogs import verification
from cogs import guildconfig


class NSAmbassador(commands.Bot):
    logger: logging.Logger
    client: pymongo.MongoClient

    def __init__(self, *, intents: discord.Intents):
        super().__init__(command_prefix=[], intents=intents)
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"NSAmbassador running discord.py {discord.__version__}")

    async def setup_hook(self):
        self.client = pymongo.MongoClient(config.MONGODB_URI)
        await self.add_cog(guildconfig.GuildConfig(self))
        await self.add_cog(verification.Verification(self))
    
    async def on_ready(self):
        assert self.user is not None
        self.logger.info(f"Logged in as {self.user} (ID: {self.user.id})")


if __name__ == "__main__":
    intents: discord.Intents = discord.Intents.default()
    bot: discord.Client = NSAmbassador(intents=intents)

    bot.run(config.BOT_TOKEN, log_level=config.LOG_LEVEL, root_logger=True)