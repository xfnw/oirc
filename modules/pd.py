

async def pd(self,c,n,m):

    if n in ['tildebot','BitBot','xfnw'] and m == '・゜゜・。。・゜゜\\_o< QUACK!':
        self.duckmsg[c] = 0
        print('duck in',c)
    elif c in self.duckmsg:
        self.duckmsg[c] += 1
        if self.duckmsg[c] == 200:
            await self.notice(self.ducknotif,'i predict there will be a duck in {} soon'.format(c))

async def init(self):
    self.raw['pd'] = pd
    self.ducknotif='xfnw'
    self.duckmsg = {}
