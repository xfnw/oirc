async def helpParse(self, c, n, m):
    if m in self.help:
        self.more[c] = self.help[m][1]
        await self.message(c, "[\x036help\x0f] " + self.help[m][0])
    else:
        await self.message(
            c,
            "[\x036help\x0f] my nice commands are {}".format(
                ", ".join([i for i in self.help if not " " in i])
            ),
        )


async def more(self, c, n, m):
    if c in self.more:
        moretext = self.more.pop(c)
        if len(moretext) > 300:
            self.more[c] = moretext[250:]
            moretext = moretext[:250] + " (more)"

        await self.message(c, "[\x036help\x0f] " + moretext)
        return
    else:
        await self.message(c, "[\x036help\x0f] there is no more more text lmao stop")


async def init(self):
    self.cmd["help"] = helpParse
    self.cmd["more"] = more

    self.help["help"] = [
        "help command - list commands or show info about one",
        "i hope this was helpful",
    ]
    self.help["help command"] = [
        "help <command> - show more info about a command (more)",
        "there is even a more, for a even more in depth look!",
    ]
    self.help["more"] = [
        "more - see more stuff when there is (more)",
        "good job you did it lol",
    ]

    self.more = {}
