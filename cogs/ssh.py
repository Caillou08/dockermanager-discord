import discord
import paramiko
import os
from discord.ext import commands
from discord import app_commands

class ssh(commands.Cog):
    host = "89.89.171.81"
    username = "root"
    password = "pG230804"
    port="10022"
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
        await self.bot.tree.sync(guild=discord.Object(id=1064226985116704829))
        print("SSH cog synced.") 

    @app_commands.command(name="senddockerlist", description="Gives the list of active container")
    async def sendDockerList(self, interaction : discord.Interaction):
        self.getDockerListFile()
        await interaction.response.send_message(file=discord.File("output.txt"))
        os.remove("output.txt")
        self.client.close()

    @app_commands.command(name="sendcommandtocontainer", description="Send a command to a container via SSH protocol")
    async def sendCommandToContainer(self, interaction : discord.Interaction, container:str, command:str):
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.host, username=self.username, password=self.password, port=self.port)
        _stdin, _stdout,_stderr = self.client.exec_command(f"docker exec {container} {command}")
        await interaction.response.send_message(f"Logs : `{_stdout.read().decode()}`")

    @app_commands.command(name="restartcontainer")
    async def restartContainer(self, interaction :discord.Interaction, container:str):
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.host, username=self.username, password=self.password, port=self.port)
        _stdin, _stdout, _stderr = self.client.exec_command(f"docker restart {container}")
        await interaction.response.send_message("Restart request send to the container")

    @app_commands.command(name="mccommand")
    async def McCommand(self, interaction :discord.Interaction, command:str):
        self.getDockerListFile()
        testvar=False
        with open('output.txt', 'r') as f:
            for line in f.readlines():
                if "tccr.io/truecharts/minecraft-java" in line:
                    testvar=True
                    self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    self.client.connect(self.host, username=self.username, password=self.password, port=self.port)
                    _stdin, _stdout, _stderr = self.client.exec_command(f"docker exec {line[0:12]}  mc-send-to-console {command}")
                    f.close()
                    os.remove("output.txt")
                    if len(_stdout.read().decode())>0:
                        await interaction.response.send_message(f"Logs : `{_stdout.read().decode()}`")
                    else :
                        await interaction.response.send_message(f"Nothing were printed in the console but the command was send succesfully.")
        if testvar==False:
            await interaction.response.send_message(f"No TrueCharts minecraft container were found. Maybe check the docker container list.")

    @app_commands.command(name="getmcconsolelogs")
    async def getMcConsoleLogs(self, interaction=discord.Interaction):
        self.getDockerListFile()
        with open('output.txt', 'r') as f:
            for line in f.readlines():
                if "tccr.io/truecharts/minecraft-java" in line:
                    self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    self.client.connect(self.host, username=self.username, password=self.password, port=self.port)
                    _stdin, _stdout, _stderr = self.client.exec_command(f"docker logs {line[0:12]}")
                    OFile = open("outputLogs.txt", "a")
                    OFile.write(_stdout.read().decode())
                    OFile.close()
                    await interaction.response.send_message(file=discord.File("outputLogs.txt"))
                    os.remove("outputLogs.txt")
                    self.client.close()
        os.remove("output.txt")

async def setup(bot):
    await bot.add_cog(ssh(bot), guilds=[discord.Object(id=1064226985116704829)])