import discord
from discord.ext import commands
import time

class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='ping', help='Menampilkan latensi bot yang detail.')
    async def ping(self, ctx: commands.Context):
        """
        Mengukur dan menampilkan latensi API dan Websocket bot dengan UI yang lebih baik.
        """
        # 1. Buat embed awal untuk memberi tahu pengguna bahwa proses sedang berjalan
        embed = discord.Embed(
            title="🏓 Pinging...",
            description="Mengukur latensi ke server Discord...",
            color=discord.Color.greyple()
        )
        
        # 2. Kirim pesan dan catat waktu
        start_time = time.monotonic()
        message = await ctx.send(embed=embed)
        end_time = time.monotonic()
        
        # 3. Hitung latensi
        api_latency = round((end_time - start_time) * 1000)
        websocket_latency = round(self.bot.latency * 1000)
        
        # 4. Tentukan warna embed berdasarkan total latensi
        total_latency = api_latency + websocket_latency
        if total_latency < 200:
            color = discord.Color.green()
        elif total_latency < 400:
            color = discord.Color.yellow()
        else:
            color = discord.Color.red()
            
        # 5. Buat embed hasil akhir yang sudah diperbarui
        final_embed = discord.Embed(
            title="🏓 Pong!",
            color=color
        )
        
        # Menambahkan field untuk setiap jenis latensi
        final_embed.add_field(
            name="🌐 Latensi API", 
            value=f"```ini\n{api_latency} ms\n```", 
            inline=True
        )
        final_embed.add_field(
            name="❤️ Latensi Websocket", 
            value=f"```ini\n{websocket_latency} ms\n```", 
            inline=True
        )
        
        final_embed.set_footer(text=f"Diminta oleh {ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)
        final_embed.timestamp = discord.utils.utcnow() # Menambahkan timestamp saat ini

        # 6. Edit pesan awal dengan embed hasil akhir
        await message.edit(embed=final_embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))