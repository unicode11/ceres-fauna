import discord
from discord.ext import commands
from discord import app_commands
import json

with open("user_data_example.json", "r") as f:
    user_data = json.load(f)
    
class rq_acc(commands.Cog):
  def __init__(self, bot):
        self.bot = bot

  @app_commands.command(name="request_access", description="Для получения ключа доступа к прокси.")
  async def request_access(self, interaction: discord.Interaction):
      user_id = str(interaction.user.id)
  
      if user_id in user_data:
          credentials = user_data[user_id]
          await interaction.user.send(
              f"**Логин:** {credentials['login']}\n\n"
              f"**Первое подключение:**\n`{credentials['proxy1']}`\n\n**Второе подключение:**\n`{credentials['proxy2']}`\n\n"
              f"Гайд: https://discord.com/channels/1191842612169162933/1294696891497451520/1296083254956265572\n\n"
              f"Пользуйся!"
          )
          await interaction.response.send_message(":green_circle: Логин найден. Данные для подключения в яичке.", ephemeral=True)
      else:
          await interaction.response.send_message(":red_circle: Доступ не предоставлен. Обратись к администратору.", ephemeral=True)
          
  @commands.Cog.listener()
  async def on_ready(self):
    await self.bot.tree.sync()
        
        
async def setup(bot):
  await bot.add_cog(rq_acc(bot))