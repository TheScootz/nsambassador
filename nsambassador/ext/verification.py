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

    @app_commands.command()
    async def verify(self, interaction: discord.Interaction):
        if (await self.fetch_usernation(interaction.user.id)) is None:
            await interaction.response.send_modal(VerificationModal())

    async def fetch_usernation(self, userid: int) -> Optional[dict]:
        record = await self.bot.database.fetchrow(
            "SELECT nation, settings FROM usernation WHERE snowflake = $1", userid
        )
        return None if record is None else dict(record)


class VerificationModal(discord.ui.Modal, title="Verify"):
    nation = discord.ui.Label(
        text="Nation Name",
        description='Hello! To verify, please provide your nation\'s name on NationStates ("Name" field in Settings).',
        component=discord.ui.TextInput(placeholder="Enter Nation Name"),
    )

    async def on_submit(self, interaction: discord.Interaction):
        assert isinstance(self.nation.component, discord.ui.TextInput)
        await interaction.response.send_message(f"Hi {self.nation.component.value}")


async def setup(bot: NSAmbassador):
    await bot.add_cog(Verification(bot=bot))
