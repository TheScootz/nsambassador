import logging
import secrets
from typing import Optional

import asyncpg
import discord
from discord import app_commands
from discord.ext import commands

from nsambassador.nsambassador import NSAmbassador

TOKEN_SALT = secrets.token_hex()


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
            await interaction.response.send_modal(GetNationModal(self))

    async def fetch_usernation(self, userid: int) -> Optional[dict]:
        record = await self.bot.database.fetchrow(
            "SELECT nation, settings FROM usernation WHERE snowflake = $1", userid
        )
        return None if record is None else dict(record)


### UI ELEMENTS ###


class GetNationModal(discord.ui.Modal, title="Your Nation"):
    def __init__(self, verification: Verification):
        super().__init__()
        self.verification = verification
        self.nation = discord.ui.Label(
            text="Nation Name",
            description='Your nation\'s name on NationStates ("Name" field in Settings).',
            component=discord.ui.TextInput(placeholder="Enter Nation Name"),
        )

        self.add_item(self.nation)

    async def on_submit(self, interaction: discord.Interaction):
        assert isinstance(self.nation.component, discord.ui.TextInput)
        await interaction.response.send_message(
            view=VericodeLinkView(self.verification, self.nation.component.value),
            ephemeral=True,
        )


class VericodeLinkView(discord.ui.LayoutView):
    def __init__(self, verification: Verification, nation: str):
        super().__init__()
        self.verification = verification
        self.nation = nation

        text = discord.ui.TextDisplay(
            f'To verify your NationStates nation, you need your Verification Code. You can find it by clicking the button below. Once you have it, press "Verify" to finish verifying.'
        )
        self.action_row = discord.ui.ActionRow()

        self.action_row.add_item(
            discord.ui.Button(
                label="Get Verification Code",
                style=discord.ButtonStyle.primary,
                url=f"https://www.nationstates.net/page=verify_login?token={hash(nation + TOKEN_SALT)}",
            )
        )
        self.action_row.add_item(
            VerifyButton(modal=GetVericodeModal(self.verification, self.nation))
        )

        self.add_item(text)
        self.add_item(self.action_row)


class VerifyButton(discord.ui.Button):
    def __init__(self, modal: discord.ui.Modal):
        super().__init__()
        self.label = "Verify"
        self.style = discord.ButtonStyle.success
        self.modal = modal

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(self.modal)
        assert isinstance(self.view, discord.ui.LayoutView)
        self.view.stop()


class GetVericodeModal(discord.ui.Modal, title="Finish Verifying"):
    def __init__(self, verification: Verification, nation: str):
        super().__init__()
        self.nation = nation
        self.vericode = discord.ui.Label(
            text="Verification Code",
            description="Your Verification Code from NationStates",
            component=discord.ui.TextInput(placeholder="Enter Verification Code"),
        )

        self.add_item(self.vericode)

    async def on_submit(self, interaction: discord.Interaction):
        assert isinstance(self.vericode.component, discord.ui.TextInput)
        await interaction.response.send_message(
            f"Nation: {self.nation}, Verification Code: {self.vericode.component.value}"
        )


async def setup(bot: NSAmbassador):
    await bot.add_cog(Verification(bot=bot))
