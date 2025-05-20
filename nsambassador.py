import asyncio
import discord
import os
import pymongo

# Load .env variables
from dotenv import load_dotenv
load_dotenv()

class NSAmbassador(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self, fallback_to_global=True)

    async def setup_hook(self):
        ...
    
    async def on_ready(self):
        print("Ready to take commands!")

intents = discord.Intents.default()
bot = NSAmbassador(intents=intents)

@bot.tree.command()
async def say(interaction: discord.Interaction, msg: str):
    await interaction.response.send_message(msg)

if __name__ == "__main__":
    bot.run(os.getenv("BOT_TOKEN"))