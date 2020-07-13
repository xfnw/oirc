import modules.identify as ident
import asyncio

async def bal(self):
    bals = {'bank':self.initfund}
    for t in self.ledger:
        await asyncio.sleep(0) # yeild control as this is a long operation
        t['amount'] = float(t['amount'])
        if t['amount'] < 0.01:
            self.ledger.delete(id=t['id'])
            continue # dont send negative money lol
        if t['sender'] not in bals:
            bals[t['sender']]=0.00
        if t['to'] not in bals:
            bals[t['to']]=0.00

        if bals[t['sender']] - t['amount'] < 0.0:
            self.ledger.delete(id=t['id'])
            continue # no debt for you
        bals[t['sender']] += 0 - t['amount']
        bals[t['to']] += t['amount']
    return bals

async def send(self,c,n,m):
    m = m.split(' ')
    if len(m) < 2:
        await self.message(c, '[\x036admin\x0f] invalid syntax')
        return
    to = await ident.user(self, m.pop(0))
    amount = float(m.pop(0))
    message = ' '.join(m)
    sender = await ident.user(self, n)

    self.ledger.insert(dict(to=to,sender=sender,amount=amount,message=message))

    await self.message(c, '[\x036admin\x0f] added transaction to ledger, check balances to verify')

async def balance(self,c,n,m):
    m = m.strip()
    if len(m) < 1:
        m = n
    try:
        m = await ident.user(self, m)
    except:
        m = m
    bals = await bal(self)
    if m in bals:
        await self.message(c, '[\x036coin\x0f] {}\u200c{}\'s balance is {} BUUT (BalUn Useless Tokens), {}% of the total supply'
                .format(m[:1],m[1:],bals[m],int((bals[m]/self.initfund)*100)))
    else:
        await self.message(c, '[\x036coin\x0f] this user has never made a transaction')

async def richest(self,c,n,m):
    richest = sorted((await bal(self)).items(), key=lambda item: item[1], reverse=True)[:10]

    await self.message(c, '[\x036coin\x0f] richest users: '+', '.join(
        [
            i[0][:1]+"\u200c"+i[0][1:]+": "+str(i[1])
            for i in richest]
        ))

async def init(self):
    self.ledger = self.db['ledger']
    self.initfund = 100.00


    self.cmd['sendcoins'] = send
    self.cmd['balance'] = balance
    self.cmd['richest'] = richest



    self.help['sendcoins'] = ['sendcoins <recipient> <amount> [message] - send someone coins. note (more)','this does NOT verify transactions went through!! check your balance after']
    self.help['balance'] = ['balance [person] - check someone\'s balance','coins owo']
    self.help['richest'] = ['richest - who has the most coins','coins owo']

