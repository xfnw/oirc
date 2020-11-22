import asyncio 
from bot import *

@command('test')
@is_admin
async def testy(self,channel,nick,msg):
    await message(self,'test',channel,str(bot.hi))
    bot.hi += 1

async def init(self):

    await self.send_raw("join #bots")
    

