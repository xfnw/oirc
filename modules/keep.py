from bot import *
import random


async def getkeep(self, c, n, m):
    m = m.strip()
    if len(m) < 1:
        keep = random.choice([i["keep"] for i in self.keepdb.find()])
    else:
        try:
            keep = random.choice(
                [i["keep"] for i in self.keepdb.find(keep={"like": "%{}%".format(m)})]
            )
        except IndexError:
            await self.message(c, "No keeps found.")
            return
    await self.message(c, keep)


async def grabkeep(self, c, n, m):
    if len(m) < 1:
        m = "1"
    try:
        back = int(m) + 0
    except:
        m = m.strip().split(" ")
        if c in self.owolog:
            backlog = [i for i in self.owolog[c] if m[0] == i[0]]
            if len(backlog) < 1:
                await self.message(c, "nothing found to keep")
                return
            try:
                ms = backlog[0 - int(m[1])]
            except:
                ms = backlog[-1]
            m = "<{}> {}".format(ms[0], ms[1])
            self.keepdb.insert(dict(channel=c, nick=n, keep=m))
            await self.message(c, "keep added!")
        return
    if c in self.owolog and len(self.owolog[c]) >= back:
        ms = self.owolog[c][0 - back]
        m = "<{}> {}".format(ms[0], ms[1])
    else:
        await self.message(
            c, "My backlog does not go back that far ;_;]"
        )
        return
    self.keepdb.insert(dict(channel=c, nick=n, keep=m))
    await self.message(c, "keep added!")


async def addkeep(self, c, n, m):
    self.keepdb.insert(dict(channel=c, nick=n, keep=m))
    await self.message(c, "keep added!")


async def rmkeep(self, c, n, m):
    if (
        n in self.channels[self.rmkeepchan].users
        and "o" in self.channels[self.rmkeepchan].users[n].modes
    ):
        co = m.strip().split(" ")
        if len(co) < 2:
            await self.message(c, "wrong syntax")
            return
        crit = co.pop(0)
        filt = " ".join(co)
        if crit == "nick" or crit == "n":
            ou = self.keepdb.delete(nick=filt)
        elif crit == "quote" or crit == "q":
            ou = self.keepdb.delete(keep={"like": filt})
        else:
            await self.message(c, "invalid criterea")
        if ou:
            await self.message(c, "removed some keep(s)")
        else:
            await self.message(c, "did not find any to remove")
    else:
        await self.message(c, f"you must have +o in {self.rmkeepchan}")


async def init(self):
    self.keepdb = shared.db["keep"]

    shared.commands["keep"] = getkeep
    # self.help['keep'] = ['keep - get keeps about keep','lets learn about keep!']

    shared.commands["addkeep"] = addkeep
    # self.help['addkeep'] = ['addkeep <keep> - add a new keep (more)','if you find something offensive contact lickthecheese, he can remove it and/or tell you who added it so watch out!']

    shared.commands["grabkeep"] = grabkeep
    # self.help['grabkeep'] = ['grabkeep [back] - grab something to keep','tooootally did not steal this from bitbot']

    self.rmkeepchan = "#balun"
    shared.commands["rmkeep"] = rmkeep
    # self.help['rmkeep'] = ['rmkeep <criteria> <pattern> - remove some keep(s). criteria types in (more)','types of criteria: n|nick q|quote eg "rmkeep nick spammer" to get rid of all keeps created by nick spammer']
