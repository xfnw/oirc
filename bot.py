#!/usr/bin/env python3

import asyncio, os, importlib

from irctokens import build, Line
from ircrobots import Bot as BaseBot
from ircrobots import Server as BaseServer
from ircrobots import ConnectionParams, SASLUserPass, SASLSCRAM

from auth import username, password

class Server(BaseServer):
    async def line_read(self, line: Line):
        print(f"{self.name} < {line.format()}")
        if 'on_'+line.command.lower() in dir(self):
            await self.__getattribute__('on_'+line.command.lower())(line)
    async def line_send(self, line: Line):
        print(f"{self.name} > {line.format()}")


    async def on_001(self, line):
        asyncio.create_task(self.load_modules())


    async def load_modules(self):
        self.modules = {}
        self.listeners = []
        self.commands = {}
        for i in [s for s in os.listdir('modules') if '.py' in s and '.swp' not in s]:
            i = i[:-3]
            m = __import__('modules.' + i)
            m = eval('m.' + i)
            asyncio.create_task(m.init(self))
            self.modules[i] = m







class Bot(BaseBot):
    def create_server(self, name: str):
        return Server(self, name)


async def main():
    bot = Bot()

    sasl_params = SASLUserPass(username, password)
    params      = ConnectionParams(
        "balun",
        host = "irc.tilde.chat",
        port = 6697,
        tls  = True,
        sasl = sasl_params)

    await bot.add_server("tilde", params)
    await bot.run()

if __name__ == "__main__":
    asyncio.run(main())

