import json

import discord
from discord import app_commands
from discord.ext import commands

from config import *

def save(id: int, name: str, filename=USERS_PATH):
    data_user = {
        str(id): {
            "login": name,
            "proxy1": "value1",
            "proxy2": "value2",
        }
    }

    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    data.update(data_user)

    with open(filename, 'w', encoding='utf-8') as f:
        print(f"saving {data}")
        json.dump(data, f, ensure_ascii=False, indent=4)


class add_user(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="add_user", description="ROOT_ADD_USER_CMD.")
    @app_commands.describe(user="Пользователь (Находящийся на сервере)(В случае если его нет на сервере - ввести ID)")
    @app_commands.describe(name="Логин (косметическое)")
    async def add_user(self, interaction: discord.Interaction,
                       user: discord.Member ,
                       name: str
                       ):
        if not(str(interaction.user.id) == Config.Read(ROOT_PATH, "ROOT_ID")):
            await interaction.response.send_message(":x:.", ephemeral=True)
            return
        
        if user != str:
            if name == None: name = user.name
        elif user == str:
            if name == None: name = user
        else:
            await interaction.response.send_message("Такого дебила нет или ничего не было введено", ephemeral=True)

        save(user.id, name)
        print(f"Подключила {user} {user.id}, {user.name}")
        await interaction.response.send_message(f"Успешно! {user} теперь крокодил.", ephemeral=True)


    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()


async def setup(bot):
    await bot.add_cog(add_user(bot))
