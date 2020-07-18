import asyncio

async def on_join(self,channel,person):
    if person in self.users:
        user = self.users[person]
        self.userdb.insert_ignore(dict(user),['id'])

async def on_all(self,wtime=100):
    print('will index users in ',wtime)
    await asyncio.sleep(wtime)
    print('started indexing users')
    users = self.users
    for person in users:
        user = self.users[person]
        await asyncio.sleep(0)
        self.userdb.insert_ignore(dict(user),['id'])
    print('done')

async def findalt(self,c,n,m):
    m = m.strip()
    user = self.userdb.find_one(nickname={'like':m},order_by='-id')
    if user == None:
        await self.message(c,'[\x036usrinfo\x0f] I could not find that user :(')
    # check if identd
    if user['username'][0] == '~':
        # not identd
        alts = [i['nickname'] for i in self.userdb.find(hostname=user['hostname'])]
    else:
        alts = [i['nickname'] for i in self.userdb.find(username=user['username'])]
    if len(alts) < 2:
        await self.message(c,'[\x036usrinfo\x0f] I could not find any alts :(')
        return
    falt=' '.join([i[:1]+'\u200c'+i[1:] for i in sorted(list(set(alts)))])
    if len(falt) > 200:
        if c in self.more:
            self.more[c].append(falt[400:])
        else:
            self.more[c] = [falt[400:]]
        falt = falt[:400]+' (more)'
    await self.message(c,'[\x036usrinfo\x0f] alts: {}'.format(falt))

async def init(self):
    self.userdb = self.db['user']

    if not self.userdb.find_one(sync='yes'):
        self.userdb.insert(dict(sync='yes'))
        asyncio.get_event_loop().create_task(on_all(self))

    self.help['findalt'] = ['findalt <nick> - find out who someone\'s alts are',';p']
    self.cmd['findalt'] = findalt
