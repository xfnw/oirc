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

async def init(self):
    self.userdb = self.db['user']

    if not self.userdb.find_one(sync='yes'):
        self.userdb.insert(dict(sync='yes'))
        asyncio.get_event_loop().create_task(on_all(self))
