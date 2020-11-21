
async def user(self,nick):
    u = await self.whois(nick)
    if u and u['account']:
        return u['account']
    else:
        raise Exception('NotLoggedIn')

async def init(self):
    pass


