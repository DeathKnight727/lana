import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from typing import Dict, List

# --- Type Hinting ---
# Mendefinisikan kelas bot kustom agar Pylance mengenali atribut tambahan
class BotWithMusicAttrs(commands.Bot):
    queues: Dict[int, List[dict]]
    current_song: Dict[int, dict]

# --- Setup Awal ---
TOKEN = os.getenv('DISCORD_TOKEN')

# Path sekarang relatif terhadap lokasi file ini
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Inisialisasi Bot ---
intents = discord.Intents.default()
intents.voice_states = True # Wajib untuk fitur suara

bot = BotWithMusicAttrs(command_prefix="!", intents=intents, help_command=None)

# Membuat state manager untuk musik yang bisa diakses semua cog
bot.queues = {}
bot.current_song = {}

# --- Event Handler dan Fungsi Utama ---
@bot.event
async def on_ready():
    """Event yang dijalankan saat bot berhasil terhubung ke Discord."""
    await bot.change_presence(activity=discord.Game(name="/help untuk bantuan"))
    
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    try:
        await load_cogs()
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash command(s).")
    except Exception as e:
        print(f"Failed to sync slash commands: {e}")
    print('Bot is ready!')

# Fungsi untuk memuat semua Cogs secara rekursif
async def load_cogs():
    """Memuat semua cogs dari folder cogs dan sub-foldernya."""
    cogs_path = os.path.join(BASE_DIR, 'cogs')
    
    for root, dirs, files in os.walk(cogs_path):
        for filename in files:
            if filename.endswith('.py') and not filename.startswith('__'):
                # Membuat path modul python (contoh: bot_lana.cogs.music.player)
                module_path = os.path.relpath(root, os.path.join(BASE_DIR, '..')).replace(os.sep, '.') + f'.{filename[:-3]}'
                
                try:
                    await bot.load_extension(module_path)
                    print(f'Loaded cog: {module_path}')
                except Exception as e:
                    print(f'Failed to load cog {module_path}: {e}')
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from typing import Dict, List

# --- Type Hinting ---
# Mendefinisikan kelas bot kustom agar Pylance mengenali atribut tambahan
class BotWithMusicAttrs(commands.Bot):
    queues: Dict[int, List[dict]]
    current_song: Dict[int, dict]

# --- Setup Awal ---
TOKEN = os.getenv('DISCORD_TOKEN')

# Path sekarang relatif terhadap lokasi file ini
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Inisialisasi Bot ---
intents = discord.Intents.default()
intents.voice_states = True # Wajib untuk fitur suara

bot = BotWithMusicAttrs(command_prefix="!", intents=intents, help_command=None)

# Membuat state manager untuk musik yang bisa diakses semua cog
bot.queues = {}
bot.current_song = {}

# --- Event Handler dan Fungsi Utama ---
@bot.event
async def on_ready():
    """Event yang dijalankan saat bot berhasil terhubung ke Discord."""
    await bot.change_presence(activity=discord.Game(name="/help untuk bantuan"))
    
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    try:
        await load_cogs()
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash command(s).")
    except Exception as e:
        print(f"Failed to sync slash commands: {e}")
    print('Bot is ready!')

# Fungsi untuk memuat semua Cogs secara rekursif
async def load_cogs():
    """Memuat semua cogs dari folder cogs dan sub-foldernya."""
    cogs_path = os.path.join(BASE_DIR, 'cogs')
    
    for root, dirs, files in os.walk(cogs_path):
        for filename in files:
            if filename.endswith('.py') and not filename.startswith('__'):
                # Membuat path modul python (contoh: bot_lana.cogs.music.player)
                module_path = os.path.relpath(root, os.path.join(BASE_DIR, '..')).replace(os.sep, '.') + f'.{filename[:-3]}'
                
                try:
                    await bot.load_extension(module_path)
                    print(f'Loaded cog: {module_path}')
                except Exception as e:
                    print(f'Failed to load cog {module_path}: {e}')
