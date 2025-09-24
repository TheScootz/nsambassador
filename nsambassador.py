import asyncio
import json
import logging

import asyncpg
import discord
import nationstates
from discord.ext import commands

import nsaconfig


class NSAmbassador(commands.Bot):
    logger: logging.Logger
    database: asyncpg.Connection

    def __init__(self, *, intents: discord.Intents):
        super().__init__(command_prefix=[], intents=intents)
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"NSAmbassador running discord.py {discord.__version__}")

    async def setup_hook(self):
        self.database = await asyncpg.connect(nsaconfig.POSTGRES_URI)
        await self.database.set_type_codec("jsonb", encoder=json.dumps, decoder=json.loads, schema="pg_catalog")

        await self.load_extension("cogs.guildconfig")
        await self.load_extension("cogs.verification")
    
    async def on_ready(self):
        assert self.user is not None
        self.logger.info(f"Logged in as {self.user} (ID: {self.user.id})")


if __name__ == "__main__":
    intents: discord.Intents = discord.Intents.default()
    bot: discord.Client = NSAmbassador(intents=intents)

    bot.run(nsaconfig.BOT_TOKEN, log_level=nsaconfig.LOG_LEVEL, root_logger=True)