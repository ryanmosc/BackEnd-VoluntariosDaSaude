import logging
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import asyncio

load_dotenv() 
DISCORD_BOT_TOKEN = os.getenv('BOOT_DISCORD')
DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

log_queue = asyncio.Queue()

class DiscordHandler(logging.Handler):
    def emit(self, record):
        log_message = self.format(record)
        if bot.is_ready():
            bot.loop.call_soon_threadsafe(log_queue.put_nowait, log_message)

logger = logging.getLogger('API_Logger')
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s')) 
logger.addHandler(console_handler)

discord_handler = DiscordHandler()
discord_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s')) 
logger.addHandler(discord_handler)


@tasks.loop(seconds=2)
async def enviar_logs_discord():
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    while not log_queue.empty():
        msg = await log_queue.get()
        if channel:
            await channel.send(f"```{msg}```")

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    logger.info(f'Bot conectado como {bot.user}')
    enviar_logs_discord.start()

# Rodar bot
def start_bot():
    bot.run(DISCORD_BOT_TOKEN)