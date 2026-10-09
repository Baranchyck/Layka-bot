import discord
from discord.ext import commands

from services import censor_message

class Commands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._webhooks: dict[int, discord.Webhook] = {}

    async def _get_webhook(self, channel: discord.TextChannel) -> discord.Webhook:
        if channel.id in self._webhooks:
            return self._webhooks[channel.id]

        for wh in await channel.webhooks():
            if wh.user == self.bot.user:
                self._webhooks[channel.id] = wh
                return wh

        wh = await channel.create_webhook(name="Censor")
        self._webhooks[channel.id] = wh
        return wh

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or message.guild is None:
            return

        censored_text, is_modified = censor_message(message.content)
        if not is_modified:
            return

        try:
            await message.delete()
            webhook = await self._get_webhook(message.channel)
            await webhook.send(
                content=censored_text,
                username=message.author.display_name,
                avatar_url=message.author.display_avatar.url,
                allowed_mentions=discord.AllowedMentions.none(),
            )
        except discord.Forbidden:
            print(f"[Помилка прав] Потрібні Manage Messages і Manage Webhooks в #{message.channel}")
        except discord.HTTPException as e:
            print(f"[Помилка Discord API] {e}")
            
async def setup(bot: commands.Bot):
    await bot.add_cog(Commands(bot))