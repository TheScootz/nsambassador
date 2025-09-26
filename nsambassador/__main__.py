import discord

from . import config, nsambassador

intents: discord.Intents = discord.Intents.default()
bot: discord.Client = nsambassador.NSAmbassador(intents=intents)

bot.run(config.BOT_TOKEN, log_level=config.LOG_LEVEL, root_logger=True)