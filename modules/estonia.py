
import random

async def getfact(self,c,n,m):
  fact = random.choice([i['fact'] for i in self.est.find()])
  await self.message(c,'[\x036estonia\x0f] fact: {}'.format(fact))

async def addfact(self,c,n,m):
  self.est.insert(dict(channel=c,nick=n,fact=m))
  await self.message(c,'[\x036estonia\x0f] fact added!')


async def init(self):
  self.est = self.db['estonia']

  self.cmd['fact'] = getfact
  self.help['fact'] = ['fact - get facts about estonia','lets learn about estonia!']
  
  self.cmd['addfact'] = addfact
  self.help['addfact'] = ['addfact <fact> - add a new fact (more)','if you find something offensive contact lickthecheese, he can remove it and/or tell you who added it so watch out!']


