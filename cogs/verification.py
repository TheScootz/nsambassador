import logging

import discord
from discord import app_commands
from discord.ext import commands

from nsambassador import NSAmbassador

class Verification(commands.Cog):
    bot: NSAmbassador
    logger: logging.Logger

    def __init__(self, bot: NSAmbassador):
        self.bot = bot
        self.logger = logging.getLogger(__name__)
    
    # @app_commands.command()
    # async def setup(self, interaction: discord.Interaction):


    @app_commands.command()
    async def say(self, interaction: discord.Interaction, msg: str):
        await interaction.response.send_message(msg)


async def setup(bot: NSAmbassador):
    await bot.add_cog(Verification(bot=bot))