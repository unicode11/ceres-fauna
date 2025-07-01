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
    "add_user",
    "linux_perf",
    "payment",
    # "faq"
]

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"{bot.user}")


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f":x: oopsie woopsie we got a fucky wucky\n{error}")


@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    await interaction.response.send_message(f":x:\n\n{error}", ephemeral=True)


async def main():
    print(">> LOAD")
    async with bot:
        for cog in cogs:
            await bot.load_extension(f'{cog}')
            print(f"{cog}")
        print(">> DONE")

        await bot.start(read(ROOT_PATH)["token"])


asyncio.run(main())
