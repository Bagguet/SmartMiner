import threading
import asyncio
import discord
import os
from dotenv import load_dotenv
from utils import log

load_dotenv()
TOKEN = os.getenv('DC_API_KEY')
DC_USER_ID_str = os.getenv('DC_USER_ID')

if not TOKEN:
    raise ValueError("DC_API_KEY environment variable is not set")
if not DC_USER_ID_str:
    raise ValueError("DC_USER_ID environment variable is not set")

DC_USER_ID = int(DC_USER_ID_str)

# Setup Bot
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

def send_dm(message):
    """Safely sends a DM from a different thread."""
    if bot.loop and bot.is_ready():
        asyncio.run_coroutine_threadsafe(_send_dm_async(message), bot.loop)
        log("[Discord] Bot sent DM")
    else:
        log("[Discord] Bot is not ready yet.")

async def _send_dm_async(message):
    try:
        user = await bot.fetch_user(DC_USER_ID)
        await user.send(message)
    except Exception as e:
        log(f"[Discord Error] {e}")

@bot.event
async def on_ready():
    log(f'[INFO] Discord Bot logged in as {bot.user}')

def start_discord_bot():
    thread = threading.Thread(target=bot.run, args=(TOKEN,), daemon=True)
    thread.start()