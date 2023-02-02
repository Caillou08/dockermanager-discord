import discord, os, asyncio
from discord import app_commands
from discord.ext import commands

intents=discord.Intents.all()
intents.message_content=True 

class MyBot(commands.Bot):

    commands_list=[]

    async def on_ready(self):
        print(f"-> {self.user} is connected. -> Average ping : {round(self.latency*1000)}ms. -> {len(self.commands_list)} cogs found.")
    
    async def setup_hook(self):
        print("Trying to load and sync all cogs, this might take a moment.")
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f"cogs.{filename[:-3]}")
                self.commands_list.append(filename[:-3])

bot=MyBot(command_prefix="!", intents=intents, application_id="1067199646591631360")

bot.run("MTA2NzE5OTY0NjU5MTYzMTM2MA.GQvhJ_.KxfzjgtfoTtcqaAmHTEc2parMVOeW6c12U8Z9k")  