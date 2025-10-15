import logging

import discord
from discord import app_commands
from discord.ext import commands

from nsambassador.nsambassador import NSAmbassador


class GuildManager(commands.Cog):
    bot: NSAmbassador
    logger: logging.Logger

    def __init__(self, bot: NSAmbassador):
        self.bot = bot
        self.logger = logging.getLogger(__name__)

    @commands.Cog.listener()
    async def on_guild_available(self, guild: discord.Guild):
        # Synchronize commands with servers
        # TODO Do this differently
        self.bot.tree.copy_global_to(guild=guild)
        self.bot.tree.clear_commands(guild=guild)
        await self.bot.tree.sync(guild=guild)
        self.logger.debug(f"Synched commands to guild {guild.name} (ID: {guild.id})")

        record = await self.bot.database.fetchval(
            "SELECT settings FROM guild WHERE snowflake = $1", guild.id
        )
        assert isinstance(record, dict)
        self.bot.settings[guild.id] = record

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        self.logger.info(f"Joined guild {guild.name} (ID: {guild.id})")
        # Add guild to DB if it's not already there
        if (
            await self.bot.database.fetchrow(
                "SELECT * FROM guild WHERE snowflake = $1", guild.id
            )
        ) is None:
            try:
                await self.bot.database.execute(
                    "INSERT INTO guild (snowflake) VALUES ($1)", guild.id
                )
            except Exception as e:
                self.logger.exception(
                    f"Error adding guild {guild.name} to database, leaving"
                )
                await guild.leave()
                return
            self.logger.info(f"Guild {guild.name} added to database")
        else:
            self.logger.info(f"Guild {guild.name} already exists in database")

    @app_commands.command()
    async def set(self, interaction: discord.Interaction, name: str, *, value: str):
        """Placeholder command to set guild settings."""
        if interaction.is_guild_integration():
            assert interaction.guild_id is not None
            self.bot.settings[interaction.guild_id][name] = value
            await self.bot.database.execute(
                "UPDATE guild SET settings = $1::jsonb WHERE snowflake = $2",
                self.bot.settings[interaction.guild_id],
                interaction.guild_id
            )


async def setup(bot: NSAmbassador):
    await bot.add_cog(GuildManager(bot=bot))
