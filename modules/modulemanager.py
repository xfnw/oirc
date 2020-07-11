

async def listMods(self,c,n,m):
  await self.message(c,'[\x036modulemanager\x0f] currently loaded mods: {}'.format(list(self.modules.keys())))

async def source(self,c,n,m):
    if m == self.nickname+': source':
        await self.message(c,'[\x036modulemanager\x0f] My source is at https://xfnw.ttm.sh/git/oirc/')



async def init(self):
  self.help['modules'] = ['modules - list the modules',':o']
  self.cmd['modules'] = listMods
  self.raw['source'] = source


