import uuid
import requests
import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View
from yoomoney import Client
from config import *

CLIENT = Client(Config.Read(ROOT_PATH, "YOOMONEY_TOKEN"))
YM = Config.Read(ROOT_PATH, "YOOMONEY_ID")
WB = Config.Read(ROOT_PATH, "WEBHOOK_URL")
YM_URL = "https://yoomoney.ru/quickpay/confirm"
GIF = "https://cdn.discordapp.com/attachments/1149826600167297135/1226869385323483136/14.gif?ex=6856a3a7&is=68555227&hm=2f960382d560aa7e09dc7f8350f17841d0b53457cc20cd041e362c2c651c7030&"


def create_payment_link(receiver: str, amount: float) -> tuple[str, str]:
    label = str(uuid.uuid4())
    link = (
        f"https://yoomoney.ru/quickpay/confirm?"
        f"receiver={receiver}&quickpay-form=button&paymentType=AC&sum={amount:.2f}&label={label}"
    )
    return link, label

def notify_payment(user_id, label):
    embed = {
        "title": f"<@{user_id}>",
        "color": 0x00FF00,
        "fields": [
            {"name": "Label", "value": f"`{label}`", "inline": True},
        ],
    }

    payload = {"embeds": [embed]}

    try:
        response = requests.post(WB, json=payload)
        if response.status_code != 204 and response.status_code != 200:
            print(f"{response.status_code}, {response.text}")
    except Exception as e:
        print(e)

def check_payment(label: str, user_id: int) -> bool:
    try:
        operations = CLIENT.operation_history(label=label, records=1)
        if operations and operations.operations:
            op = operations.operations[0]  
            if op.status == 'success':
                notify_payment(user_id, label)
                return True
        return False
    except Exception as e:
        print(f"крайная пизда наступила: {e}")
        return False


class Payment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="pay", description="Оплата сервиса.")
    async def pay(self, interaction: discord.Interaction, amount: float):
        if amount <= 10 and not interaction.user.id == Config.Read(ROOT_PATH, "ROOT_ID"):
            await interaction.response.send_message(
                "Введена слишком маленькая сумма! ~~Нищеброд ебанный~~",
                ephemeral=True
            )
            return
        
        payment_link, label = create_payment_link(YM, amount)

        await interaction.user.send(GIF)

        button = Button(label="Проверить пизду", style=discord.ButtonStyle.green)

        async def button_callback(interaction_button: discord.Interaction):
            if check_payment(label, interaction.user.id):
                await interaction_button.response.send_message(
                    "✅", ephemeral=True
                )
            else:
                await interaction_button.response.send_message(
                    "❌ Платёж не найден или ещё не завершён.", ephemeral=True
                )

        button.callback = button_callback
        view = View()
        view.add_item(button)

        await interaction.response.send_message(
            f"К оплате: **{amount}₽**\nСсылка для оплаты: {payment_link}\n~~Уникальный label: `{label}`~~",
            ephemeral=True,
            view=view
        )
        notify_payment(interaction.user.id, label)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()


async def setup(bot):
    await bot.add_cog(Payment(bot))
