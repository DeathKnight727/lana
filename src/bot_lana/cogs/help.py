import discord
from discord import app_commands
from discord.ext import commands
from typing import cast

# --- Type Hinting ---
# Diperlukan agar Pylance tahu tipe `bot`
class BotWithMusicAttrs(commands.Bot):
    pass

# --- Cog untuk Perintah Bantuan ---
class Help(commands.Cog):
    def __init__(self, bot: BotWithMusicAttrs):
        self.bot = bot

    @app_commands.command(name="help", description="Menampilkan semua perintah yang tersedia.")
    async def help(self, interaction: discord.Interaction):
        """Menampilkan pesan bantuan yang dinamis untuk semua slash command."""
        
        embed = discord.Embed(
            title="🤖 Bantuan Perintah Bot",
            description="Berikut adalah daftar semua slash command yang tersedia:",
            color=discord.Color.blue()
        )

        # Mengelompokkan perintah berdasarkan Cog
        # Ini akan membuat kategori seperti "Music", "General", dll. secara otomatis
        cogs = {}
        for command in self.bot.tree.get_commands():
            cog_name = command.cog_name or "General"
            if cog_name not in cogs:
                cogs[cog_name] = []
            
            # Menambahkan detail perintah ke dalam list
            cogs[cog_name].append(f"`/{command.name}` - {command.description}")

        # Menambahkan field ke embed untuk setiap kategori
        for cog_name, commands_list in cogs.items():
            if commands_list:
                embed.add_field(
                    name=f"**{cog_name}**",
                    value="\n".join(commands_list),
                    inline=False
                )
        
        # Mengirim embed sebagai respons yang hanya bisa dilihat oleh pengguna
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: BotWithMusicAttrs):
    await bot.add_cog(Help(bot))
