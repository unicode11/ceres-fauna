import discord
from config import *

class System:
    def __init__(self, name): 
        self.name = name
    
    async def CheckRoot(id):
        interaction: discord.Interaction
        if not(str(id) == Config.Read(ROOT_PATH, "ROOT_ID")):
            await interaction.response.send_message(":x:.", ephemeral=True)
            print(f"[SYSTEM] {interaction.user} пытался использовать команду для ROOT.")
            return