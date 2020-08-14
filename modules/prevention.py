
import random

async def plogger(self,c,n,m):
  if c not in self.plog:
    self.plog[c] = []

  self.plog[c].append([n,m])
  if len(self.plog[c]) > 50:
    del self.plog[c][:-50]


  if c in self.channels and 'o' in self.channels[c]['modes'] and self.nickname in self.channels[c]['modes']['o']:
      # fun time
      umc = len([i for i in self.plog[c][-10:] if i[0]==n])
      #await self.message(c,str(umc))
      if umc > 6:
          if n in self.wlevel:
              self.wlevel[n] += 1
          else:
              self.wlevel[n] = 0
          if self.wlevel[n] == 3:
              await self.set_mode(c,self.mutesyntax[0],self.mutesyntax[1].format(n+'!*@*'))
          if self.wlevel[n] > 10:
              self.wlevel[n] = 0
              await self.kick(c,n,'stop spamming thanks')
              
  


async def init(self):
  self.plog = {}
  self.wlevel = {}
  self.mutesyntax = ['+b','m:{}'] # ['+q','{}'] on freenode
  self.raw['preventionlog'] = plogger

