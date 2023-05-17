import discord
import paramiko
import os
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
IP = os.getenv("IP")
USER = os.getenv("USER")
PASS = os.getenv("PASS")
PORT = os.getenv("PORT")
SERVER_ID = os.getenv("SERVER_ID")

class ssh(commands.Cog):
    host = IP
    username = USER
    password = PASS
    port= PORT
    client = paramiko.client.SSHClient()

    def getDockerListFile(self):
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.host, username=self.username, password=self.password, port=self.port)
        _stdin, _stdout, _stderr = self.client.exec_command("docker container ls")
        OFile = open("output.txt", "a")
        OFile.write(_stdout.read().decode())
        OFile.close()

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("SSH cog loaded.")
        await self.bot.tree.sync(guild=discord.Object(id=SERVER_ID))
        print("SSH cog synced.") 

    @app_commands.command(name="senddockerlist", description="Gives the list of active containers.")
    async def sendDockerList(self, interaction : discord.Interaction):
        self.getDockerListFile()
        await interaction.response.send_message(file=discord.File("output.txt"))
        os.remove("output.txt")
        self.client.close()

    @app_commands.command(name="sendcommandtocontainer", description="Send a command to a container via SSH protocol.")
    async def sendCommandToContainer(self, interaction : discord.Interaction, container:str, command:str):
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.host, username=self.username, password=self.password, port=self.port)
        _stdin, _stdout,_stderr = self.client.exec_command(f"docker exec {container} {command}")
        await interaction.response.send_message(f"Logs : `{_stdout.read().decode()}`")

    @app_commands.command(name="restartcontainer", description="Restart a specific container.")
    async def restartContainer(self, interaction :discord.Interaction, container:str):
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.host, username=self.username, password=self.password, port=self.port)
        _stdin, _stdout, _stderr = self.client.exec_command(f"docker restart {container}")
        await interaction.response.send_message("Restart request send to the container")
async def setup(bot):
    await bot.add_cog(ssh(bot), guilds=[discord.Object(id=SERVER_ID)])