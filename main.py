import asyncio

import discord
from discord import app_commands
from discord.ext import commands

from config import *

intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

cogs = [
    "rq_acc",
    # "add_user",
    "linux_perf",
    "payment",
    # "edit_user",
    # "faq"
]

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"{bot.user}")

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    await interaction.response.send_message(f":x:\n\n{error}", ephemeral=True)


async def main():
    print("[BOT] >> LOAD")
    async with bot:
        for cog in cogs:
            await bot.load_extension(f'{cog}')
            print(f"[COGS] {cog}")
        print("[BOT] >> DONE")

        await bot.start(Config.Read(ROOT_PATH, "TOKEN"))


asyncio.run(main())
