import discord
from discord.ext import commands
import yt_dlp

# Kelas untuk menampung tombol-tombol kontrol
class MusicControls(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="▶️ Resume", style=discord.ButtonStyle.green)
    async def resume(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.guild is None:
            await interaction.response.send_message("Guild tidak ditemukan.", ephemeral=True)
            return
        voice_client = interaction.guild.voice_client
        if isinstance(voice_client, discord.VoiceClient) and voice_client.is_paused():
            voice_client.resume()
            await interaction.response.send_message("Lagu dilanjutkan.", ephemeral=True)
            # Ubah tombol menjadi "Pause"
            button.label = "⏸️ Pause"
            button.style = discord.ButtonStyle.secondary
            if interaction.message is not None:
                await interaction.message.edit(view=self)
        else:
            await interaction.response.send_message("Tidak ada lagu yang sedang dijeda.", ephemeral=True)

    @discord.ui.button(label="⏸️ Pause", style=discord.ButtonStyle.secondary)
    async def pause(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.guild is None:
            await interaction.response.send_message("Guild tidak ditemukan.", ephemeral=True)
            return
        voice_client = interaction.guild.voice_client
        if isinstance(voice_client, discord.VoiceClient) and voice_client.is_playing():
            voice_client.pause()
            await interaction.response.send_message("Lagu dijeda.", ephemeral=True)
            # Ubah tombol menjadi "Resume"
            button.label = "▶️ Resume"
            button.style = discord.ButtonStyle.green
            if interaction.message is not None:
                await interaction.message.edit(view=self)
        else:
            await interaction.response.send_message("Tidak ada lagu yang sedang diputar.", ephemeral=True)

    @discord.ui.button(label="⏭️ Skip", style=discord.ButtonStyle.primary)
    async def skip(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.guild is None:
            await interaction.response.send_message("Guild tidak ditemukan.", ephemeral=True)
            return
        voice_client = interaction.guild.voice_client
        if isinstance(voice_client, discord.VoiceClient) and voice_client.is_playing():
            voice_client.stop()
            await interaction.response.send_message("Lagu dilewati.", ephemeral=True)
        else:
            await interaction.response.send_message("Tidak ada lagu yang sedang diputar untuk dilewati.", ephemeral=True)

    @discord.ui.button(label="⏹️ Stop", style=discord.ButtonStyle.danger)
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.guild is None:
            await interaction.response.send_message("Guild tidak ditemukan.", ephemeral=True)
            return
        voice_client = interaction.guild.voice_client
        if voice_client:
            await voice_client.disconnect(force=False)
            await interaction.response.send_message("Pemutaran dihentikan dan bot keluar dari channel.", ephemeral=True)
            # Menonaktifkan semua tombol setelah dihentikan
            for item in self.children:
                if isinstance(item, discord.ui.Button):
                    item.disabled = True
            if interaction.message is not None:
                await interaction.message.edit(view=self)
        else:
            await interaction.response.send_message("Bot tidak sedang berada di voice channel.", ephemeral=True)


# --- Class Cog Musik Utama ---
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='play', help='Memainkan lagu dari YouTube dan menampilkan kontrol.')
    async def play(self, ctx, *, url):
        """Memainkan audio dari URL dan menampilkan panel kontrol."""
        # Jika bot belum ada di voice channel, suruh gabung
        if not ctx.voice_client:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("Anda harus berada di voice channel untuk memainkan musik.")
                return
        
        # Opsi untuk yt-dlp untuk mendapatkan audio terbaik
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        # Hentikan lagu yang sedang diputar jika ada
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        # Mencari informasi lagu
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                if not info:
                    await ctx.send("Tidak dapat menemukan informasi lagu dari URL yang diberikan.")
                    return
                audio_url = info['url']
                title = info.get('title', 'Unknown Title')
            except Exception as e:
                await ctx.send(f"Terjadi error saat mencari lagu: {e}")
                return

        # Memainkan audio
        source = discord.FFmpegPCMAudio(audio_url, before_options=FFMPEG_OPTIONS['before_options'], options=FFMPEG_OPTIONS['options'])
        ctx.voice_client.play(source)

        # Mengirim pesan embed dengan tombol kontrol
        embed = discord.Embed(title="🎶 Sedang Memutar", description=f"**{title}**", color=discord.Color.blue())
        thumbnail_url = info.get('thumbnail') if info and isinstance(info, dict) else None
        if thumbnail_url:
            embed.set_thumbnail(url=thumbnail_url)
        embed.set_footer(text=f"Diminta oleh: {ctx.author.name}")
        
        await ctx.send(embed=embed, view=MusicControls())
        
    @commands.command(name='leave', help='Bot akan keluar dari voice channel.')
    async def leave(self, ctx):
        """Membuat bot keluar dari voice channel."""
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("Berhasil keluar dari voice channel.")
        else:
            await ctx.send("Saya tidak sedang berada di voice channel.")


async def setup(bot):
    await bot.add_cog(Music(bot))