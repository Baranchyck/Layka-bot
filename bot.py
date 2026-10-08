import asyncio

import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

from db_vocabulary import censor_message, REPLACEMENTS

load_dotenv()

TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Ready {bot.user}')

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    if message.content == 'z':
        await message.reply('gojda')
    await message.channel.send('Привіт')


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    censored_text, is_modified = censor_message(message.content)

    if is_modified:
        try:
            await message.delete()

            await message.channel.send(
                f"{message.author.mention} шляхетно зазначив(-ла):\n> {censored_text}"
            )
        except discord.Forbidden:
            print(
                f"[Помилка прав] Бот не має прав видаляти повідомлення на каналі #{message.channel.name}"
            )
        except discord.HTTPException as e:
            print(f"[Помилка Discord API] {e}")

    await bot.process_commands(message)

if __name__ == "__main__":
    if not TOKEN:
        raise ValueError(
            "Токен не знайдено! Перевір наявність DISCORD_TOKEN у файлі .env"
        )
    bot.run(TOKEN)
