#!/usr/bin/env python3


import pydle, asyncio, dataset, sys, os, time

class Balun(pydle.Client):
  async def on_connect(self):
    print('Connected!')

    self.modules = {}
    self.cmd = {}
    self.rawm = {}
    self.help = {}
    self.db = dataset.connect('sqlite:///database.db')
    self.t=0

    print('loading modules...')
    await self.loadMods()
    print('joining channels')
    for i in self.chansjoin:
      await self.join(i)
    print('Done!')

    # tilde +B bot
    await self.set_mode(self.nickname, '+B')


  async def loadMods(self):
    for i in [s for s in os.listdir('modules') if ".py" in s and '.swp' not in s]:
      i = i[:-3]
      print('loading', i)
      m = __import__("modules."+i)
      m = eval('m.'+i)
      await m.init(self)
      self.modules[i] = m

  async def on_invite(self, channel, by):
    print('{} invited me to {}!'.format(by, channel))
    self.t = time.time()+1
    await self.join(channel)

  async def on_join(self, channel, person):
      await super().on_join(channel, person)
      await self.modules['usrinfo'].on_join(self,channel,person)

  async def on_ctcp(self, by, chan, what, contents):
    await self.on_message(chan,by,"{} {}".format(what,contents)) # treat ctcp as normal messages

  async def on_message(self, chan, source, msg):
    if chan == self.nickname: # dont try to message yourself when people dm you lmfao
      chan = source
    if source != self.nickname:


      if time.time() > self.t:
        

        if msg == '!botlist':
          await self.message(chan, 'helo im owen\'s nice bot https://xfnw.ttm.sh/git/oirc')
        await self.parseCommand(chan, source, msg)
      for i in self.rawm:
        await self.rawm[i](self, chan, source, msg)

  async def parseCommand(self, chan, source, msg):
    if msg[:len(self.prefix)] == self.prefix:

      msg = msg[len(self.prefix):]
      cmd = msg.split(' ')[0]
      msg = msg[len(cmd)+1:]
      if len(cmd) < 1:
        return
    
      if cmd in self.cmd:
        await self.cmd[cmd](self, chan, source, msg)
        return

      # fuzzy search for commands
      results = [i for i in self.cmd if i.startswith(cmd)]
      if len(results) == 1:
        await self.cmd[results[0]](self, chan, source, msg)


  async def is_admin(self, nickname):

    # Check the WHOIS info to see if the source has identified with NickServ.
    # This is a blocking operation, so use yield.
    info = await self.whois(nickname)
    if 'account' in info:
      account = info['account']
    else:
      # they are not nickserv registered
      return False

    return account in self.admins



if __name__ == "__main__":
  client = Balun('balun', realname='owens bot')
  client.admins = ['lickthecheese', 'ben', 'coffeeowl', 'gbmor', 'tomasino', 'ubergeek', 'deepend', 'calamitous', 'khuxkm']
  client.prefix = '.'
  client.run('team.tilde.chat', tls=True, tls_verify=False)
  
