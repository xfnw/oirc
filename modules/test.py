import asyncio 
import modules.core as core

@core.is_admin
async def testy(self,channel,nick,message):
    pass

async def init(self):

    await self.send_raw("join #bots")
    await asyncio.sleep(5)
    await testy(self,'#bots','xfnw','hi')

