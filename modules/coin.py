import asyncio
from bot import *


async def bal(self):
    bals = {}
    for t in self.ledger:
        await asyncio.sleep(0)  # yeild control as this is a long operation
        t["amount"] = float(t["amount"])
        if t["amount"] < 0.01:
            self.ledger.delete(id=t["id"])
            continue  # dont send negative money lol
        if t["sender"] not in bals:
            bals[t["sender"]] = 0.00
        if t["to"] not in bals:
            bals[t["to"]] = 0.00

        if t["sender"] != "bank" and round(bals[t["sender"]], 2) - t["amount"] < 0.0:
            self.ledger.delete(id=t["id"])
            continue  # no debt for you
        bals[t["sender"]] += 0 - t["amount"]
        bals[t["to"]] += t["amount"]

        for i in bals:
            bals["bank"] += bals[i] * 0.001
            bals[i] -= bals[i] * 0.001
    self.initfund = abs(bals["bank"])
    return bals


async def send(self, c, n, m):
    m = m.split(" ")
    if len(m) < 2:
        await self.message(c, "[\x036coin\x0f] invalid syntax")
        return
    try:
        to = self.users[m.pop(0).lower()].account
    except:
        await self.message(
            c,
            "[\x036coin\x0f] that user is not logged in. refusing so coins are not lost",
        )
    if to == "":
        await self.message(c, "[\x036coin\x0f] they must authenticate with nickserv.")
        return
    amount = round(float(m.pop(0)), 2)
    message = " ".join(m)
    sender = self.users[n.lower()].account

    self.ledger.insert(dict(to=to, sender=sender, amount=amount, message=message))

    await self.message(
        c, "[\x036coin\x0f] added transaction to ledger, check balances to verify"
    )


async def balance(self, c, n, m):
    m = m.strip()
    if len(m) < 1:
        m = n
    try:
        m = self.users[m.lower()].account
    except:
        m = m
    if m == "":
        m = m
    bals = await bal(self)
    if m in bals:
        latest = self.ledger.find_one(to=m, order_by="-id")
        if latest:
            await self.message(
                c,
                "[\x036coin\x0f] {}\u200c{}'s balance is {} BUTT (Balun Useless Trading Tokens), {}% of the total supply".format(
                    m[:1],
                    m[1:],
                    round(bals[m], 2),
                    int((bals[m] / self.initfund) * 100),
                )
                + '. last deposit: [{} from {}, "{}"]'.format(
                    latest["amount"], latest["sender"], latest["message"]
                ),
            )
        else:
            await self.message(
                c,
                "[\x036coin\x0f] {}\u200c{}'s balance is {} BUTT (Balun Useless Trading Tokens), {}% of the total supply".format(
                    m[:1],
                    m[1:],
                    round(bals[m], 2),
                    int((bals[m] / self.initfund) * 100),
                ),
            )
    else:
        await self.message(c, "[\x036coin\x0f] this user has never made a transaction")


async def richest(self, c, n, m):
    richest = sorted((await bal(self)).items(), key=lambda item: item[1], reverse=True)[
        :10
    ]

    await self.message(
        c,
        "[\x036coin\x0f] richest users: "
        + ", ".join(
            [
                i[0][:1] + "\u200c" + i[0][1:] + ": " + str(round(i[1], 2))
                for i in richest
            ]
        ),
    )


async def init(self):
    self.ledger = shared.db["ledger"]
    self.initfund = 1

    shared.commands["tipcoins"] = send
    shared.commands["sendcoins"] = send
    shared.commands["balance"] = balance
    shared.commands["richest"] = richest

    return
    self.help["sendcoins"] = [
        "sendcoins <recipient> <amount> [message] - send someone coins. note (more)",
        "this does NOT verify transactions went through!! check your balance after",
    ]
    self.help["balance"] = ["balance [person] - check someone's balance", "coins owo"]
    self.help["richest"] = ["richest - who has the most coins", "coins owo"]
