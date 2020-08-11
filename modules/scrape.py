
# '[\x0303Pronouns\x03] Pronouns for xfnw: he/him'


async def scraper(self,c,n,m):
    m = m.split(' ')
    if len(m) > 4:
        if m.pop(0) in ('[\x0303Pronouns\x03]', '[Pronouns]') and m.pop(0) == 'Pronouns' and m.pop(0) == 'for':
            person = m.pop(0)[:-1]
            pronouns = ' '.join(m)

            print('found pronouns of {}: {}'.format(person,pronouns))
            self.pronoundb.upsert(dict(nick=person,pronouns=pronouns),['nick'])

async def getPronouns(self,c,n,m):
    m = m.strip()
    if not m:
        m = n
    pronoun = self.pronoundb.find_one(nick=m)
    if pronoun:
        await self.message(c,'[\x036scrape\x0f] Pronouns for {}: {}'.format(pronoun['nick'],pronoun['pronouns']))
    else:
        await self.message(c,'[\x036scrape\x0f] sorry i could not find {}\'s pronouns. (i scrape pronouns from logs, you dont need to set them :3 )'.format(m))

async def init(self):
    self.raw['scraper'] = scraper
    self.pronoundb = self.db['pronouns']

    self.cmd['pronouns'] = getPronouns

