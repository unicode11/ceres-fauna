import discord
from discord import app_commands
from discord.ext import commands

from config import *

class edit_user(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="edit_user", description="ROOT_EDIT_USER_CMD.")
    async def edit_user(self, interaction: discord.Interaction):
        if not(str(interaction.user.id) == Config.Read(ROOT_PATH, "ROOT_ID")):
            await interaction.response.send_message(":x:.", ephemeral=True)
            return
        print("test")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()


async def setup(bot):
    await bot.add_cog(edit_user(bot))
