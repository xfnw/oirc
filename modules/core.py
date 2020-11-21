


def is_admin(func):
    async def decorator(self,channel,nick,message):
        if nick.lower() in self.users and self.users[nick.lower()].account in self.admins:
            await self.send_raw("PRIVMSG #bots :test")
    return decorator
        

#def is_chanop(func):


async def init(self):
    self.admins = ['xfnw','lickthecheese']

