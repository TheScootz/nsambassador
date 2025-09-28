import asyncio
import json
import logging

import asyncpg
import discord
import nationstates
from discord.ext import commands

import nsambassador.config as config


class NSAmbassador(commands.Bot):
    logger: logging.Logger
    database: asyncpg.Connection

    def __init__(self, *, intents: discord.Intents):
        super().__init__(command_prefix=[], intents=intents)
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"NSAmbassador running discord.py {discord.__version__}")

    async def setup_hook(self):
        self.database = await asyncpg.connect(config.POSTGRES_URI)
        await self.database.set_type_codec("jsonb", encoder=json.dumps, decoder=json.loads, schema="pg_catalog")

        await self.load_extension(".ext.guildmanager", package="nsambassador")
        await self.load_extension(".ext.verification", package="nsambassador")
    
    async def on_ready(self):
        assert self.user is not None
        self.logger.info(f"Logged in as {self.user} (ID: {self.user.id})")

def main():
    intents = discord.Intents.default()
    bot = NSAmbassador(intents=intents)

    @bot.tree.command()
    async def reload_extensions(interaction: discord.Interaction):
        await bot.reload_extension(".ext.guildmanager", package="nsambassador")
        await bot.reload_extension(".ext.verification", package="nsambassador")
        bot.logger.info("All extensions reloaded")
        await interaction.response.send_message("All extensions reloaded", ephemeral=True)

    bot.run(config.BOT_TOKEN, log_level=config.LOG_LEVEL, root_logger=True)
