import logging
from typing import Optional

import asyncpg
import discord
from discord import app_commands
from discord.ext import commands

from nsambassador.nsambassador import NSAmbassador

class Verification(commands.Cog):
    bot: NSAmbassador
    logger: logging.Logger

    def __init__(self, bot: NSAmbassador):
        self.bot = bot
        self.logger = logging.getLogger(__name__)

    @app_commands.command()
    async def say(self, interaction: discord.Interaction, msg: str):
        await interaction.response.send_message(msg)
    
    async def fetch_usernation(self, user: discord.User) -> Optional[dict]:
        record = await self.bot.database.fetchrow("SELECT nation, settings FROM usernation WHERE snowflake = $1", user.id)
        return (None if record is None else dict(record))


async def setup(bot: NSAmbassador):
    await bot.add_cog(Verification(bot=bot))