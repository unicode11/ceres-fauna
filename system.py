import discord
from config import *

class Bot:
    def __init__(self, name): 
        self.name = name
    
    async def checkRoot(id):
        interaction: discord.Interaction
        if not(str(id) == Config.Read(ROOT_PATH, "ROOT_ID")):
            await interaction.response.send_message(":x:.", ephemeral=True)
            return