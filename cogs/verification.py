import logging

import discord
from discord import app_commands
from discord.ext import commands


class Verification(commands.Cog):
    bot: commands.Bot
    logger: logging.Logger

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)

    @app_commands.command()
    async def say(self, interaction: discord.Interaction, msg: str):
        await interaction.response.send_message(msg)


async def setup(bot: commands.Bot):
    await bot.add_cog(Verification(bot=bot))