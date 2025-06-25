import json
import uuid
import requests
from typing import Optional
import discord
import urllib.parse
from discord import app_commands
from discord.ext import commands

from config import *

YM = read(ROOT_PATH)["yoomoney_id"]
WB = read(ROOT_PATH)["webhook"]
YM_URL = "https://yoomoney.ru/quickpay/confirm"
GIF = "https://cdn.discordapp.com/attachments/1149826600167297135/1226869385323483136/14.gif?ex=6856a3a7&is=68555227&hm=2f960382d560aa7e09dc7f8350f17841d0b53457cc20cd041e362c2c651c7030&"

def send(data: dict):
    """
    data: {
        "discord_id": int,
        "username": str,
        "amount": float,
        "label": str,
        "operation_id": str
    }
    """
    embed = {
        "title": "💰 Новая оплата",
        "color": 0x00ff00,
        "fields": [
            {"name": "Пользователь", "value": f"{data['username']} (`{data['discord_id']}`)", "inline": False},
            {"name": "Сумма", "value": f"{data['amount']} ₽", "inline": True},
            {"name": "Label", "value": data['label'], "inline": True}
        ]
    }

    payload = {
        "embeds": [embed]
    }

    response = requests.post(WB, json=payload)
    
    if response.status_code != 204 and response.status_code != 200:
        print(f"{response.status_code}\n{response.text}")
    else:
        print("отправлено")

def link(receiver: str, username: str, amount: float) -> tuple[str, str]:
    label = str(uuid.uuid4())

    params = {
        "receiver": receiver,
        "quickpay-form": "button",
        "paymentType": "AC",  # банковская карта, еще есть mc но я его рот ебал
        "sum": f"{amount:.2f}",
        "label": label
    }

    full_url = f"{YM_URL}?{urllib.parse.urlencode(params, quote_via=urllib.parse.quote)}"
    return full_url, label

# def check(label: str) -> Optional[dict]:
#     headers = {
#         "Authorization": f"Bearer {read(ROOT_PATH)["yoomoney_token"]}"
#     }

#     response = requests.post(
#         "https://yoomoney.ru/api/operation-history",
#         headers=headers,
#         json={"label": label}
#     )

#     if response.status_code != 200:
#         print(f"{response.status_code}, {response.text}")
#         return None

#     data = response.json()
#     operations = data.get("operations", [])

#     for op in operations:
#         if (
#             op.get("label") == label and
#             op.get("status") == "success" and
#             float(op.get("amount", 0))
#         ):
#             return op 

#     return None

class payment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="pay", description="Оплата сервиса.")
    async def payment(self, 
                      interaction: discord.Interaction,
                      amount: float):
        payment_url, label = link(
            receiver=YM,
            username=interaction.user,
            amount=amount
        )

        penis = {
            "discord_id": interaction.user.id,
            "username": str(interaction.user),
            "amount": amount,
            "label": label,
            # "operation_id": result["operation_id"]
        }
        send(penis)
        
        # with open("payments.json", "a", encoding="utf-8") as f:
        #     f.write(json.dumps(penis) + "\n")
        await interaction.user.send(WB)
        await interaction.response.send_message(
            f"К оплате: **{amount}₽**, {payment_url}\n~~Уникальный label для этой оплаты - `{label}` (сохраните его для проверки оплаты)~~ <- Забей хуй, пока в разработке /shrug",
            ephemeral=True
        )
        
    @app_commands.command(name="check_payment",description="Проверить оплату.")
    async def check_payment(self, interaction: discord.Interaction, label: str):
        if not(str(interaction.user.id) == read(ROOT_PATH)["root_id"]):
            await interaction.response.send_message("Команда в разработке.", ephemeral=True)
            return

        await interaction.response.defer(thinking=True)
        # result = check(label)


        # if not result:
        #     await interaction.followup.send("❌ Платёж не найден или ещё не обработан.")
        #     return
        # await interaction.followup.send("✅ Оплата успешно подтверждена и записана.")



    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()


async def setup(bot):
    await bot.add_cog(payment(bot))
