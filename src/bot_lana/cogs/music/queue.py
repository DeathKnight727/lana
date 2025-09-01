import discord
from discord import app_commands
from discord.ext import commands
from typing import Dict, List

# --- Type Hinting ---
# Mendefinisikan kelas bot kustom agar Pylance mengenali atribut tambahan
class BotWithMusicAttrs(commands.Bot):
    queues: Dict[int, List[dict]]
    current_song: Dict[int, dict]

# --- Cog untuk Mengelola Antrean ---
class Queue(commands.Cog, name="Music"):
    def __init__(self, bot: BotWithMusicAttrs):
        self.bot = bot

    @app_commands.command(name="queue", description="Menampilkan antrean lagu saat ini.")
    async def queue(self, interaction: discord.Interaction):
        # Memastikan perintah dijalankan di server
        if not interaction.guild:
            return await interaction.response.send_message("Perintah ini hanya bisa digunakan di server.", ephemeral=True)
            
        guild_id = interaction.guild.id
        # Menggunakan .get() untuk akses yang aman
        queue = self.bot.queues.get(guild_id)
        
        if not queue:
            return await interaction.response.send_message("Antrean lagu kosong.", ephemeral=True)
            
        embed = discord.Embed(title="📜 Antrean Lagu", color=discord.Color.purple())
        
        # Menampilkan hingga 10 lagu
        for i, song in enumerate(queue[:10]):
            embed.add_field(name=f"{i+1}. {song['title']}", value=f"Diminta oleh: {song['requester']}", inline=False)
            
        if len(queue) > 10:
            embed.set_footer(text=f"... dan {len(queue) - 10} lagu lainnya.")
            
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="skip", description="Melewati lagu yang sedang diputar.")
    async def skip(self, interaction: discord.Interaction):
        if not interaction.guild:
            return await interaction.response.send_message("Perintah ini hanya bisa digunakan di server.", ephemeral=True)

        vc = interaction.guild.voice_client
        if isinstance(vc, discord.VoiceClient) and vc.is_playing():
            vc.stop() # Menghentikan lagu akan memicu fungsi 'after' di play_next
            await interaction.response.send_message("Lagu dilewati.", ephemeral=True)
        else:
            await interaction.response.send_message("Tidak ada lagu yang sedang diputar untuk dilewati.", ephemeral=True)
        
    @app_commands.command(name="nowplaying", description="Menampilkan lagu yang sedang diputar.")
    async def nowplaying(self, interaction: discord.Interaction):
        if not interaction.guild:
            return await interaction.response.send_message("Perintah ini hanya bisa digunakan di server.", ephemeral=True)
        
        guild_id = interaction.guild.id
        current_song = self.bot.current_song.get(guild_id)
        
        if current_song:
            embed = discord.Embed(title="🎶 Sedang Memutar", description=f"**{current_song['title']}**", color=discord.Color.blue())
            if current_song.get('thumbnail'):
                embed.set_thumbnail(url=current_song['thumbnail'])
            embed.set_footer(text=f"Diminta oleh: {current_song['requester']}")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Tidak ada lagu yang sedang diputar.", ephemeral=True)
        
async def setup(bot: BotWithMusicAttrs):
    await bot.add_cog(Queue(bot))

