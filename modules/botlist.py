from bot import *

modulename = "botlist"


@rawm("botlist")
async def botlist(s, c, n, m):
    if m == "!botlist":
        await message(s, c, "hi im balun ; prefix . ; owner xfnw")


async def init(self):
    await self.send(build("MODE", [self.nickname, "+B"]))
