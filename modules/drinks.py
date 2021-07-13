import random

from bot import *


async def coffeeup(self,c,n,m):
    m = m.lower()
    c = c.lower()
    if c in ['#coffee','#tea','#water','#caps','#sodawater']:
        if (
                (c[1:]+"!" in m and c+'!' not in m)
                or c=='#coffee' and ('latte!' in m or 'espresso!' in m or 'cappucino!' in m)
                or c=='#tea' and ('chai!' in m or 'kombucha!' in m)
                ):
            cc = self.coffee.find_one(name=c)
            if cc:
                self.coffee.update(dict(name=c,value=cc['value']+1),['name'])
            else:
                self.coffee.insert(dict(name=c,value=1))
            if c=='#CAPS':
                await message(self, c, '・゜゜・。。・゜゜c[~] {} UP!'.format(c[1:].upper()).upper())
            else:
                await message(self, c, '・゜゜・。。・゜゜c[~] {} UP!'.format(c[1:].upper()))
        elif "cupcount" in m:
            await message(self, c, '{} delicious cups of {}{} served so far!'.format(
                self.coffee.find_one(name=c)['value'], random.choice(self.coffeetypes), c[1:]
                ))




async def init(self):
    shared.rawm['coffeeup'] = coffeeup
    self.coffee = shared.db['coffee']

    self.coffeetypes = [
            "kum\u200cquat's aeropressed ",
            "hot ",
            "OSHA-compliant ",
            "cmc\u200ccabe's nom nom nom yummy ",
            "healthy ",
            ]
    for i in range(len(self.coffeetypes)):
        self.coffeetypes.append('')




