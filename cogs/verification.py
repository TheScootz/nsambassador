import discord
from discord.ext import commands

class Verification(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def say(interaction: discord.Interaction, msg: str):
        await interaction.response.send_message(msg)