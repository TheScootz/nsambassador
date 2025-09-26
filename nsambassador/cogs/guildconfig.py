import logging

import discord
from discord.ext import commands

from nsambassador.nsambassador import NSAmbassador


class GuildConfig(commands.Cog):
    bot: NSAmbassador
    logger: logging.Logger
    
    def __init__(self, bot: NSAmbassador):
        self.bot = bot
        self.logger = logging.getLogger(__name__)

    @commands.Cog.listener()
    async def on_guild_available(self, guild: discord.Guild):
        # Synchronize commands with servers
        await self.bot.tree.sync(guild=guild)
        self.logger.info(f"Synched commands to guild {guild.name} (ID: {guild.id})")
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        self.logger.info("Joined guild {} (ID: {})".format(guild.name, guild.id))
        # Add guild to DB if it's not already there
        if (await self.bot.database.fetchrow("SELECT * FROM guild WHERE snowflake = $1", guild.id)) is None:
            try:
                await self.bot.database.execute("INSERT INTO guild (snowflake) VALUES ($1)", guild.id)
            except Exception as e:
                self.logger.exception(f"Error adding guild {guild.name} to database, leaving")
                await guild.leave()
                return
            self.logger.info(f"Guild {guild.name} added to database")
        else:
            self.logger.info(f"Guild {guild.name} already exists in database")


async def setup(bot: NSAmbassador):
    await bot.add_cog(GuildConfig(bot=bot))