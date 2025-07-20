import discord
from discord import app_commands
from discord.ext import commands
import json
from config import *

FAQ = Config.read(FAQ_PATH)

class faq_ui(discord.ui.View):
    def __init__(self, category, questions, user, timeout=60):
        super().__init__(timeout=timeout)
        self.category = category
        self.questions = list(questions.items())
        self.user = user
        self.index = 0
        
    def format_embed(self):
        q, a = self.questions[self.index]
        embed = discord.Embed(
            title=f"{self.category}",
            description=f"**{q}**\n{a}",
            color=discord.Color.blurple()
        )
        embed.set_footer(text=f"{self.index + 1} / {len(self.questions)}")
        return embed
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.user:
            await interaction.response.send_message(":x:.", ephemeral=True)
            return False
        return True
    
    
    @discord.ui.button(label="◀️", style=discord.ButtonStyle.secondary)
    async def previous(self, interaction: discord.Interaction):
        if self.index > 0:
            self.index -= 1
            await interaction.response.edit_message(embed=self.format_embed(), view=self)
            
    @discord.ui.button(label="▶️", style=discord.ButtonStyle.secondary)
    async def next(self, interaction: discord.Interaction):
        if self.index < len(self.questions) - 1:
            self.index += 1
            await interaction.response.edit_message(embed=self.format_embed(), view=self)
            
# хуйня нечитабельная            

class faq(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.faq = FAQ
        
    def categories(self) -> list:
        return list(self.faq.keys())
        
    @app_commands.command(name="faq", description="Просмотреть список частозадаваемых вопросов (Чаще всего - решение проблем, связанных с подключением).")
    @app_commands.describe(category="Категория вопросов")
    async def faq(self, interaction: discord.Interaction, category: str):
        print("да я еблан")
        # data = self.faq.get(category)
        # if not data:
        #     await interaction.response.send_message("Такой категории не существует или произошла ошибка.", ephemeral=True)
        #     return
        
        # view = faq_ui(category, data, interaction.user)
        # await interaction.response.send_message(embed=view.format_embed(), view=view, ephemeral=True)        
        
    
    # @faq.autocomplete('category')
    # async def faq_autocomplete(self, interaction: discord.Interaction, current: str): # я вчера твою мать ебал
    #     return [
    #         app_commands.Choice(name=cat, value=cat)
    #         for cat in self.categories()
    #         if current.lower() in cat.lower()
    #     ]
        
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()


async def setup(bot):
    await bot.add_cog(faq(bot))
