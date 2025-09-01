import discord
from discord.ext import commands
import os
import json
from dotenv import load_dotenv

# --- Setup Awal ---
# Memastikan file settings.json ada
SETTINGS_FILE = 'settings.json'
if not os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump({}, f)

# Memuat variabel dari file .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# --- Fungsi untuk Mendapatkan Prefix ---
# Fungsi ini akan memeriksa prefix khusus server, jika tidak ada, pakai prefix default
def get_prefix(bot, message):
    # Muat prefix default dari config.json
    with open('config.json', 'r') as f:
        config = json.load(f)
        default_prefix = config.get('prefix', '!') # Default '!' jika tidak ditemukan

    # Muat settings server dari settings.json
    with open(SETTINGS_FILE, 'r') as f:
        settings = json.load(f)
    
    # Dapatkan prefix untuk guild ini, jika ada. Jika tidak, gunakan default.
    guild_id = str(message.guild.id)
    return settings.get(guild_id, {}).get('prefix', default_prefix)


# --- Inisialisasi Bot ---
# Menentukan Intents (izin yang dibutuhkan bot)
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

# Membuat instance Bot dengan prefix dinamis
bot = commands.Bot(command_prefix=get_prefix, intents=intents)

# --- Event Handler dan Fungsi Utama ---
@bot.event
async def on_ready():
    if bot.user is not None:
        print(f'Logged in as {bot.user.name}')
    else:
        print('Logged in, but bot.user is None')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash command(s).")
    except Exception as e:
        print(f"Failed to sync slash commands: {e}")
    print('Bot is ready!')

# Fungsi untuk memuat semua Cogs dari folder cogs
async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'Loaded cog: {filename}')
            except Exception as e:
                print(f'Failed to load cog {filename}: {e}')

# Menjalankan bot
async def main():
    await load_cogs()
    if TOKEN is None:
        raise ValueError("DISCORD_TOKEN is not set in the environment variables or .env file.")
    await bot.start(TOKEN)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())