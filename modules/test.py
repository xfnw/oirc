import asyncio
import bot


@bot.command("test")
@bot.is_admin
async def testy(self, channel, nick, msg):
    await bot.message(self, channel, "hi there")


async def init(self):

    await self.send_raw("join #bots")
