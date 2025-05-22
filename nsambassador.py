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
    client: pymongo.MongoClient

    def __init__(self, *, intents: discord.Intents):
        super().__init__(command_prefix=[], intents=intents)
        dotenv.load_dotenv()

    async def setup_hook(self):
        self.client = pymongo.MongoClient(os.environ["MONGO_URL"])
        await self.add_cog(guildconfig.GuildConfig(self))
        await self.add_cog(verification.Verification(self))
    
    async def on_ready(self):
        assert self.user is not None
        print(f"Logged in as {self.user} (ID: {self.user.id})")
    
    async def on_guild_available(self, guild: discord.Guild):
        # Synchronize commands with servers
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)


if __name__ == "__main__":
    intents: discord.Intents = discord.Intents.default()
    bot: discord.Client = NSAmbassador(intents=intents)

    print(f"Running discord.py {discord.__version__}")
    bot.run(os.environ["BOT_TOKEN"], log_level=os.getenv("LOG_LEVEL", logging.NOTSET)) # type: ignore