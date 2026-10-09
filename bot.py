import asyncio

import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

class MyBot(commands.Bot):
    async def setup_hook(self):
        await self.load_extension('commands')

bot = MyBot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Ready {bot.user}')


if __name__ == "__main__":
    if not TOKEN:
        raise ValueError(
            "Токен не знайдено! Перевір наявність DISCORD_TOKEN у файлі .env"
        )
    bot.run(TOKEN)