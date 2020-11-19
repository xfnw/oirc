import random


async def coffeeup(self,c,n,m):
    if c in ['#coffee','#tea','#water','#CAPS','#sodawater']:
        if (c[1:]+"!" in m and c+'!' not in m) or c=='#coffee' and ('latte!' in m or 'espresso!' in m or 'cappucino!' in m) or c=='#tea' and ('chai!' in m):
            cc = self.coffee.find_one(name=c)
            if cc:
                self.coffee.update(dict(name=c,value=cc['value']+1),['name'])
            else:
                self.coffee.insert(dict(name=c,value=1))
            if c=='#CAPS':
                await self.message(c, '[\x036drinks\x0f] ・゜゜・。。・゜゜c[~] {} UP!'.format(c[1:].upper()).upper())
            else:
                await self.message(c, '[\x036drinks\x0f] ・゜゜・。。・゜゜c[~] {} UP!'.format(c[1:].upper()))
        elif "cupcount" in m:
            await self.message(c, '[\x036drinks\x0f] {} delicious cups of {}{} served so far!'.format(
                self.coffee.find_one(name=c)['value'], random.choice(self.coffeetypes), c[1:]
                ))




async def init(self):
    self.rawm['coffeeup'] = coffeeup
    self.coffee = self.db['coffee']

    self.coffeetypes = [
            "kum\u200cquat's aeropressed ",
            "hot ",
            "OSHA-compliant ",
            "cmc\u200ccabe's nom nom nom yummy ",
            "healthy ",
            ]
    for i in range(len(self.coffeetypes)):
        self.coffeetypes.append('')




