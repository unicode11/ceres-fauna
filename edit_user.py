from config import *
import discord
from discord.ext import commands
from discord import app_commands
import json

with open(USERS_PATH, "r") as f:
    user_data = json.load(f)
    
class edit_user(commands.Cog):
  def __init__(self, bot):
        self.bot = bot

  @app_commands.command(name="edit_user", description="ROOT_EDIT_USER_CMD.")
  async def edit_user(self, interaction: discord.Interaction):
    print("test")
          
  @commands.Cog.listener()
  async def on_ready(self):
    await self.bot.tree.sync()
        
        
async def setup(bot):
  await bot.add_cog(edit_user(bot))