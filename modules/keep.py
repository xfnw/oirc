
import random

async def getkeep(self,c,n,m):
  if len(m) < 1:
    keep = random.choice([i['keep'] for i in self.keepdb.find()])
  else:
    try:
      keep = random.choice([i['keep'] for i in self.keepdb.find(keep={'like':"%{}%".format(m)})])
    except IndexError:
      await self.message(c,'[\x036keep\x0f] No keeps found.')
      return
  await self.message(c,'[\x036keep\x0f] {}'.format(keep))


async def grabkeep(self,c,n,m):
  if len(m) < 1:
    m="1"
  try:
    back = int(m)+0
  except:
    m = m.strip().split(' ')
    if c in self.owolog:
      backlog = [i for i in self.owolog[c] if m[0] == i[0]]
      if len(backlog) < 1:
        await self.message(c,'[\x036keep\x0f] nothing found to keep')
        return
      try:
        ms = backlog[0-int(m[1])]
      except:
        ms = backlog[-1]
      m = "<{}> {}".format(ms[0],ms[1])
      self.keepdb.insert(dict(channel=c,nick=n,keep=m))
      await self.message(c,'[\x036keep\x0f] keep added!')
    return
  if c in self.owolog and len(self.owolog[c]) >= back:
    ms = self.owolog[c][0-back]
    m = "<{}> {}".format(ms[0],ms[1])
  else:
    await self.message(c,'[\x036keep\x0f] My backlog does not go back that far ;_;]')
    return
  self.keepdb.insert(dict(channel=c,nick=n,keep=m))
  await self.message(c,'[\x036keep\x0f] keep added!')




async def addkeep(self,c,n,m):
  self.keepdb.insert(dict(channel=c,nick=n,keep=m))
  await self.message(c,'[\x036keep\x0f] keep added!')

async def rmkeep(self,c,n,m):
  if n in self.channels[self.rmkeepchan]['modes']['o']:
    co = m.strip().split(' ')
    if len(co) < 2:
      await self.message(c,'[\x036keep\x0f] wrong syntax')
      return
    crit = co.pop(0)
    filt = ' '.join(co)
    if crit == 'nick' or crit == 'n':
      ou = self.keepdb.delete(nick=filt)
    elif crit == 'keep' or crit == 'f':
      ou = self.keepdb.delete(keep={'like':filt})
    else:
      await self.message(c,'[\x036keep\x0f] invalid criterea')
    if ou:
      await self.message(c, '[\x036keep\x0f] removed some keep(s)')
    else:
      await self.message(c, '[\x036keep\x0f] did not remove any')
  else:
    await self.message(c,'[\x036keep\x0f] you must have +o in #keep')

async def init(self):
  self.keepdb = self.db['keep']

  self.cmd['keep'] = getkeep
  self.help['keep'] = ['keep - get keeps about keep','lets learn about keep!']
  
  self.cmd['addkeep'] = addkeep
  self.help['addkeep'] = ['addkeep <keep> - add a new keep (more)','if you find something offensive contact lickthecheese, he can remove it and/or tell you who added it so watch out!']

  self.cmd['grabkeep'] = grabkeep
  self.help['grabkeep'] = ['grabkeep [back] - grab something to keep','tooootally did not steal this from bitbot']

  self.rmkeepchan = "#o"
  self.cmd['rmkeep'] = rmkeep
  self.help['rmkeep'] = ['rmkeep <criteria> <pattern> - remove some keep(s). criteria types in (more)','types of criteria: n|nick f|keep eg "rmkeep nick spammer" to get rid of all keeps created by nick spammer']

