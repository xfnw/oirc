
import random

async def getfact(self,c,n,m):
  if len(m) < 1:
    fact = random.choice([i['fact'] for i in self.est.find()])
  else:
    try:
      fact = random.choice([i['fact'] for i in self.est.find(fact={'like':"%{}%".format(m)})])
    except IndexError:
      await self.message(c,'[\x036estonia\x0f] No facts found.')
      return
  await self.message(c,'[\x036estonia\x0f] fact: {}'.format(fact))

async def addfact(self,c,n,m):
  self.est.insert(dict(channel=c,nick=n,fact=m))
  await self.message(c,'[\x036estonia\x0f] fact added!')

async def rmfact(self,c,n,m):
  if n in self.channels[self.rmfactchan]['modes']['o']:
    co = m.strip().split(' ')
    if len(co) < 2:
      await self.message(c,'[\x036estonia\x0f] wrong syntax')
      return
    crit = co.pop(0)
    filt = ' '.join(co)
    if crit == 'nick' or crit == 'n':
      ou = self.est.delete(nick=filt)
    elif crit == 'fact' or crit == 'f':
      ou = self.est.delete(fact={'like':filt})
    else:
      await self.message(c,'[\x036estonia\x0f] invalid criterea')
    if ou:
      await self.message(c, '[\x036estonia\x0f] removed some fact(s)')
    else:
      await self.message(c, '[\x036estonia\x0f] did not remove any')
  else:
    await self.message(c,'[\x036estonia\x0f] you must have +o in #estonia')

async def init(self):
  self.est = self.db['estonia']

  self.cmd['fact'] = getfact
  self.help['fact'] = ['fact - get facts about estonia','lets learn about estonia!']
  
  self.cmd['addfact'] = addfact
  self.help['addfact'] = ['addfact <fact> - add a new fact (more)','if you find something offensive contact lickthecheese, he can remove it and/or tell you who added it so watch out!']

  self.rmfactchan = "#estonia"
  self.cmd['rmfact'] = rmfact
  self.help['rmfact'] = ['rmfact <criteria> <pattern> - remove some fact(s). criteria types in (more)','types of criteria: n|nick f|fact eg "rmfact nick spammer" to get rid of all facts created by nick spammer']

