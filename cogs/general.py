import discord
from discord.ext import commands

# Membuat class Cog untuk perintah umum
class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping', help='Menampilkan latensi bot.')
    async def ping(self, ctx):
        """Perintah sederhana untuk memeriksa apakah bot responsif."""
        latency = round(self.bot.latency * 1000)  # dalam milidetik
        await ctx.send(f'Pong! 🏓 Latensi: {latency}ms')

# Fungsi setup yang dipanggil saat Cog dimuat
async def setup(bot):
    await bot.add_cog(General(bot))