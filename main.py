import asyncio
from dotenv import load_dotenv
import os

# Memuat .env sebelum mengimpor bot agar token tersedia
load_dotenv()

# Impor bot dari paket kita di dalam src
# Pastikan nama folder "bot_lana" sudah benar
from bot_lana.bot import bot, TOKEN 

def main():
    """Fungsi utama untuk menjalankan bot."""
    if not TOKEN:
        raise ValueError("DISCORD_TOKEN tidak diatur di file .env.")
    
    try:
        # Menjalankan bot dengan tokennya
        asyncio.run(bot.start(TOKEN))
    except KeyboardInterrupt:
        print("Bot sedang dimatikan.")

if __name__ == '__main__':
    main()
