from config import *
import discord
from discord.ext import commands
from discord import app_commands
import json
import subprocess

with open(ROOT_PATH, "r") as f:
    root_data = json.load(f)
   
possible_commands = [
    "systemctl restart discord_bot.service",
    "reboot"
    
]
    
def run(cmd: str):
    try:
        result = subprocess.run(cmd,
            shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return e.stdout, e.stderr
    
class linux_perf(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @app_commands.command(name="cmd", description="ROOT_TERMINAL_CMD.")
  @app_commands.describe(command="Command to run.")
  @app_commands.choices(command=[app_commands.Choice(name=cmd, value=cmd) for cmd in possible_commands])
  async def request_access(self, interaction: discord.Interaction, *, command: str | None):
      if str(interaction.user.id) == root_data["root_id"]:
          out, err = run(command)
          if out:
              await interaction.response.send_message(f":white_check_mark:\n```{out}```", ephemeral=False)
          if err:
              await interaction.response.send_message(f":x:\n```{err}```", ephemeral=False)
      else:
          await interaction.response.send_message(":x:.", ephemeral=True)
          
  @commands.Cog.listener()
  async def on_ready(self):
    await self.bot.tree.sync()
        
        
async def setup(bot):
  await bot.add_cog(linux_perf(bot))