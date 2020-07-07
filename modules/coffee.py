import random


async def coffeeup(self,c,n,m):
    if c == '#coffee':
        if "coffee!" in m:
            cc = self.coffee.find_one(name='cupcount')
            if cc:
                self.coffee.update(dict(name='cupcount',value=cc['value']+1),['name'])
            else:
                self.coffee.insert(dict(name='cupcount',value=1))
            await self.message(c, '[\x036coffee\x0f] ・゜゜・。。・゜゜c[_] COFFEE UP!')
        elif "cupcount" in m:
            await self.message(c, '[\x036coffee\x0f] {} delicious cups of {}coffee served so far!'.format(
                self.coffee.find_one(name='cupcount')['value'], random.choice(self.coffeetypes)
                ))
    if c == '#tea':
        if "tea!" in m:
            cc = self.coffee.find_one(name='teacount')
            if cc:
                self.coffee.update(dict(name='teacount',value=cc['value']+1),['name'])
            else:
                self.coffee.insert(dict(name='teacount',value=1))
            await self.message(c, '[\x036coffee\x0f] ・゜゜・。。・゜゜[_]b TEA UP!')
        elif "cupcount" in m:
            await self.message(c, '[\x036coffee\x0f] {} delicious mugs of {}tea served so far!'.format(
                self.coffee.find_one(name='teacount')['value'], random.choice(self.coffeetypes)
                ))






async def init(self):
    self.raw['coffeeup'] = coffeeup
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




