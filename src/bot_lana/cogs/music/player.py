import discord
from discord import app_commands
from discord.ext import commands
import yt_dlp
from bot_lana.core.views import MusicControls
from typing import Dict, List

# --- Type Hinting ---
# Mendefinisikan kelas bot kustom agar Pylance mengenali atribut tambahan
class BotWithMusicAttrs(commands.Bot):
    queues: Dict[int, List[dict]]
    current_song: Dict[int, dict]

# --- Cog untuk Player ---
class Player(commands.Cog, name="Music"):
    def __init__(self, bot: BotWithMusicAttrs):
        self.bot = bot
        # Inisialisasi yang aman untuk memastikan atribut selalu ada
        if not hasattr(self.bot, "queues"):
            self.bot.queues = {}
        if not hasattr(self.bot, "current_song"):
            self.bot.current_song = {}

    # --- Fungsi Helper untuk Memutar Lagu Berikutnya ---
    def _play_next(self, interaction: discord.Interaction):
        # Pemeriksaan untuk memastikan interaksi terjadi di dalam server (guild)
        if not interaction.guild:
            return
        
        guild_id = interaction.guild.id
        queue = self.bot.queues.get(guild_id)
        
        if queue:
            vc = interaction.guild.voice_client
            if isinstance(vc, discord.VoiceClient) and not vc.is_playing():
                song = queue.pop(0)
                self.bot.current_song[guild_id] = song

                FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1', 'options': '-vn'}
                
                try:
                    source = discord.FFmpegPCMAudio(song['url'], **FFMPEG_OPTIONS)
                    vc.play(source, after=lambda e: self._play_next(interaction))
                except Exception as e:
                    print(f"Error saat memutar lagu berikutnya: {e}")
                    # Coba putar lagu selanjutnya jika terjadi error
                    return self._play_next(interaction)
                
                embed = discord.Embed(title="🎶 Sedang Memutar", description=f"**{song['title']}**", color=discord.Color.blue())
                if song.get('thumbnail'):
                    embed.set_thumbnail(url=song['thumbnail'])
                
                # Pemeriksaan tipe untuk memastikan channel bisa mengirim pesan
                if isinstance(interaction.channel, discord.abc.Messageable):
                    self.bot.loop.create_task(interaction.channel.send(embed=embed, view=MusicControls(cog=self)))
        else:
            self.bot.current_song[guild_id] = None

    @app_commands.command(name="play", description="Memutar lagu atau menambahkannya ke antrean.")
    @app_commands.describe(query="Judul atau URL lagu.")
    async def play(self, interaction: discord.Interaction, query: str):
        # Pemeriksaan yang lebih kuat untuk memastikan user adalah Member dan ada di voice channel
        if not isinstance(interaction.user, discord.Member) or not interaction.user.voice or not interaction.user.voice.channel:
            return await interaction.response.send_message("Anda harus berada di voice channel.", ephemeral=True)
        
        await interaction.response.defer()
        
        vc = interaction.guild.voice_client
        if not isinstance(vc, discord.VoiceClient):
            vc = await interaction.user.voice.channel.connect()

        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': True, 'default_search': 'ytsearch'}
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            try: 
                info = ydl.extract_info(query, download=False)['entries'][0]
            except Exception: 
                return await interaction.followup.send(f"Gagal menemukan lagu untuk `{query}`.")

        song = {'url': info['url'], 'title': info.get('title'), 'thumbnail': info.get('thumbnail'), 'requester': interaction.user.display_name}
        
        guild_id = interaction.guild.id
        if guild_id not in self.bot.queues:
            self.bot.queues[guild_id] = []
        
        self.bot.queues[guild_id].append(song)
        
        if not vc.is_playing():
            await interaction.followup.send(f"Memulai pemutaran dengan: **{song['title']}**")
            self._play_next(interaction)
        else:
            await interaction.followup.send(f"✅ Ditambahkan ke antrean: **{song['title']}**")

    @app_commands.command(name="leave", description="Membuat bot keluar dari voice channel.")
    async def leave(self, interaction: discord.Interaction):
        if not interaction.guild:
            return await interaction.response.send_message("Perintah ini hanya untuk server.", ephemeral=True)
            
        vc = interaction.guild.voice_client
        if isinstance(vc, discord.VoiceClient):
            guild_id = interaction.guild.id
            if guild_id in self.bot.queues: self.bot.queues[guild_id] = []
            if guild_id in self.bot.current_song: self.bot.current_song[guild_id] = None
            
            await vc.disconnect()
            await interaction.response.send_message("Berhasil keluar dari voice channel.")
        else:
            await interaction.response.send_message("Saya tidak sedang di voice channel.", ephemeral=True)

async def setup(bot: BotWithMusicAttrs):
    await bot.add_cog(Player(bot))

