import logging

import discord
from discord.ext import commands


class GuildConfig(commands.Cog):
    bot: commands.Bot
    logger: logging.Logger
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)

    @commands.Cog.listener()
    async def on_guild_available(self, guild: discord.Guild):
        # Synchronize commands with servers
        await self.bot.tree.sync(guild=guild)
        self.logger.info(f"Synched commands to guild {guild.name} (ID: {guild.id})")


async def setup(bot: commands.Bot):
    await bot.add_cog(GuildConfig(bot=bot))