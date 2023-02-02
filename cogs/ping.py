import discord
from discord.ext import commands
from discord import app_commands

class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Ping cog loaded.")
        await self.bot.tree.sync(guild=discord.Object(id=1064226985116704829))
        print("Ping cog synced.") 

    @app_commands.command(name="ping", description="Gives the instant ping of the bot")
    async def ping(self, interaction : discord.Interaction):
        embed = discord.Embed(
            color = discord.Color.purple()
        )
        embed.add_field(name=f"Average ping of {self.bot.user}:", value=f"My average ping is around `{round(self.bot.latency*1000)} ms`, neat right ?")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(ping(bot), guilds=[discord.Object(id=1064226985116704829)])