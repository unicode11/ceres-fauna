import discord
from discord.ext import commands
from discord import app_commands
import os
import json
    
with open("/root/discord_bot/root_data.json", "r") as f:
    root_data = json.load(f)

def save(data):
  obj = json.dumps(data, indent=4)
  print(">> USER ADD\n", data)
  try:
    with open("/root/discord_bot/user_data_add.json","w") as f:
      f.write(obj)
  except:
    print("^^^^^^ Couldn't write a file. Sorry. :c ^^^^^^^")
 
class add_user(commands.Cog):
  def __init__(self, bot):
        self.bot = bot

  @app_commands.command(name="add_user", description="ROOT_ADD_USER_CMD.")
  async def request_access(self, interaction: discord.Interaction, user: discord.User):  
      if str(interaction.user.id) == root_data["root_id"]:
        await interaction.response.send_message(f"Подключаю {user.mention}...",ephemeral=True)
        
        # ДАННЫЕ ДЛЯ ПОДКЛЮЧЕНИЯ
        login = {"login": str(user.name)}
        id = (str(interaction.user.id))
        
      else:
        await interaction.response.send_message(":x:",ephemeral=True)
          
  @commands.Cog.listener()
  async def on_ready(self):
    await self.bot.tree.sync()
        
        
async def setup(bot):
  await bot.add_cog(add_user(bot))