import discord
from discord import app_commands
from discord.ext import commands
import json
import os

# --- Helper Functions untuk Mengelola Pengaturan ---
# Path sekarang relatif terhadap file ini
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(BASE_DIR, '..', '..', 'data', 'settings.json')

# Pastikan file settings.json ada
if not os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump({}, f)

def get_guild_settings(guild_id):
    """Membaca pengaturan untuk sebuah server."""
    with open(SETTINGS_FILE, 'r') as f:
        settings = json.load(f)
    return settings.get(str(guild_id), {"autoplay": False}) # Default value

def save_guild_settings(guild_id, data):
    """Menyimpan pengaturan untuk sebuah server."""
    with open(SETTINGS_FILE, 'r') as f:
        settings = json.load(f)
    settings[str(guild_id)] = data
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)


# --- Kelas UI (View) untuk Panel Pengaturan ---
class MusicSettingsView(discord.ui.View):
    def __init__(self, guild_id):
        super().__init__(timeout=180)
        self.guild_id = guild_id
        
        # Ambil pengaturan saat ini dan update tampilan tombol
        current_settings = get_guild_settings(self.guild_id)
        autoplay_enabled = current_settings.get("autoplay", False)
        self.update_autoplay_button(autoplay_enabled)

    def update_autoplay_button(self, is_enabled):
        # Find the autoplay button by custom_id or index
        for child in self.children:
            if isinstance(child, discord.ui.Button) and getattr(child, "custom_id", None) == "autoplay_toggle":
                autoplay_button = child
                break
        else:
            autoplay_button = None

    @discord.ui.button(label="Autoplay: OFF", style=discord.ButtonStyle.secondary, custom_id="autoplay_toggle")
    async def autoplay_toggle(self, interaction: discord.Interaction, button: discord.ui.Button):
        settings = get_guild_settings(self.guild_id)
        # Toggle boolean value
        current_state = settings.get("autoplay", False)
        new_state = not current_state
        settings["autoplay"] = new_state
        save_guild_settings(self.guild_id, settings)
        
        # Update tampilan tombol dan beri respons
        if new_state:
            button.label = "Autoplay: ON"
            button.style = discord.ButtonStyle.green
        else:
            button.label = "Autoplay: OFF"
            button.style = discord.ButtonStyle.secondary
        # Edit the original response message to update the view
        try:
            await interaction.response.edit_message(view=self)
        except Exception:
            pass  # If edit_message fails, ignore

        response_message = "✅ Autoplay diaktifkan." if new_state else "❌ Autoplay dinonaktifkan."
        await interaction.followup.send(response_message, ephemeral=True)
        save_guild_settings(self.guild_id, settings)
        
        # Update tampilan tombol dan beri respons
        self.update_autoplay_button(new_state)
        try:
            await interaction.response.edit_message(view=self)
        except Exception:
            pass  # If edit_message fails, ignore

        response_message = "✅ Autoplay diaktifkan." if new_state else "❌ Autoplay dinonaktifkan."
        await interaction.followup.send(response_message, ephemeral=True)


# --- Cog untuk Perintah Settings ---
# Kita beri nama "Music" agar dikelompokkan dengan benar
class Settings(commands.Cog, name="Music"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="settings", description="Membuka panel pengaturan musik.")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def settings(self, interaction: discord.Interaction):
        """Menampilkan panel pengaturan musik interaktif."""
        embed = discord.Embed(
            title="⚙️ Pengaturan Musik",
            description="Konfigurasikan fitur musik untuk server ini.",
            color=discord.Color.orange()
        )
        embed.add_field(name="Autoplay", value="Otomatis putar lagu rekomendasi jika antrean kosong.", inline=False)
        
        if interaction.guild is not None:
            view = MusicSettingsView(interaction.guild.id)
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        else:
            await interaction.response.send_message("Perintah ini hanya dapat digunakan di dalam server.", ephemeral=True)

    @settings.error
    async def on_settings_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("Anda butuh izin `Manage Server`.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Error: {error}", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Settings(bot))