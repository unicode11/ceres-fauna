import json
import subprocess

import discord
from discord import app_commands
from discord.ext import commands

from config import *

possible_commands = [
    "systemctl restart discord_bot.service",
    "reboot",
    "echo"

]

def run(cmd: str):
    try:
        result = subprocess.run(cmd,
                                shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return e.stdout, e.stderr


class linux_perf(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="cmd", description="ROOT_TERMINAL_CMD.")
    @app_commands.describe(command="Command to run.")
    @app_commands.choices(command=[app_commands.Choice(name=cmd, value=cmd) for cmd in possible_commands])
    async def linux_perf(self, interaction: discord.Interaction, *, command: str):
        if not(str(interaction.user.id) == Config.Read(ROOT_PATH, "ROOT_ID")):
            await interaction.response.send_message(":x:.", ephemeral=True)
            return
        out, err = run(command)
        if out:
            await interaction.response.send_message(f":white_check_mark:\n```{out}```", ephemeral=False)
        if err:
            await interaction.response.send_message(f":x:\n```{err}```", ephemeral=False)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()


async def setup(bot):
    await bot.add_cog(linux_perf(bot))
