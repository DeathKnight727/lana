import discord

class MusicControls(discord.ui.View):
    # Menerima 'cog' saat inisialisasi untuk mengakses state bot
    def __init__(self, *, timeout=None, cog):
        super().__init__(timeout=timeout)
        self.cog = cog # Menyimpan referensi ke Cog

    @discord.ui.button(label="⏯️ Play/Pause", style=discord.ButtonStyle.secondary)
    async def play_pause(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.guild:
            return await interaction.response.send_message("Perintah ini hanya bisa digunakan di dalam server.", ephemeral=True)
            
        vc = interaction.guild.voice_client
        # Menambahkan pengecekan tipe untuk stabilitas dan kejelasan
        if not isinstance(vc, discord.VoiceClient):
            return await interaction.response.send_message("Bot tidak berada di voice channel.", ephemeral=True)

        if vc.is_paused():
            vc.resume()
            await interaction.response.send_message("▶️ Lagu dilanjutkan.", ephemeral=True)
        elif vc.is_playing():
            vc.pause()
            await interaction.response.send_message("⏸️ Lagu dijeda.", ephemeral=True)
        else:
            await interaction.response.send_message("Tidak ada lagu yang bisa di-pause/resume.", ephemeral=True)

    @discord.ui.button(label="⏭️ Skip", style=discord.ButtonStyle.primary)
    async def skip(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.guild:
            return await interaction.response.send_message("Perintah ini hanya bisa digunakan di dalam server.", ephemeral=True)

        vc = interaction.guild.voice_client
        if isinstance(vc, discord.VoiceClient) and vc.is_playing():
            vc.stop() # Memicu lagu selanjutnya dari antrean
            await interaction.response.send_message("Lagu dilewati.", ephemeral=True)
        else:
            await interaction.response.send_message("Tidak ada lagu yang sedang diputar untuk dilewati.", ephemeral=True)

    @discord.ui.button(label="⏹️ Stop", style=discord.ButtonStyle.danger)
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.guild:
            return await interaction.response.send_message("Perintah ini hanya bisa digunakan di dalam server.", ephemeral=True)

        vc = interaction.guild.voice_client
        if isinstance(vc, discord.VoiceClient):
            # Mengakses 'queues' melalui Cog yang sudah kita teruskan
            bot_instance = self.cog.bot
            bot_instance.queues[interaction.guild.id] = []
            bot_instance.current_song[interaction.guild.id] = None
            
            await vc.disconnect()
            await interaction.response.send_message("Pemutaran dihentikan dan antrean dikosongkan.", ephemeral=True)
        else:
            await interaction.response.send_message("Bot tidak sedang berada di voice channel.", ephemeral=True)

