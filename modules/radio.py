
import requests, asyncio


import datetime

SECOND = 1
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE
DAY = 24 * HOUR
MONTH = 30 * DAY
# https://stackoverflow.com/a/1580531
def timeDelta(dt):
    dt = datetime.datetime.fromtimestamp(dt)
    now = datetime.datetime.now()
    delta_time = dt - now

    delta =  delta_time.days * DAY + delta_time.seconds 
    minutes = delta / MINUTE
    hours = delta / HOUR
    days = delta / DAY

    if delta <  0:
        return "currently (should) be playing right now"

    if delta < 1 * MINUTE:    
      if delta == 1:
          return  "in one second"
      else:
          return str(delta) + " seconds to go"


    if delta < 2 * MINUTE:
        return "in a minute"


    if delta < 45 * MINUTE:
        return str(int(minutes)) + " minutes to go"

    if delta < 90 * MINUTE:
        return "next hour"

    if delta < 24 * HOUR:
        return str(int(hours)) + " hours to go"

    if delta < 48 * HOUR:
        return "tomorow"

    if delta < 30 * DAY:
        return str(int(days)) + " days to go"


    if delta < 12 * MONTH:
        months = delta / MONTH
        if months <= 1:
            return "one month to go"
        else:
            return str(int(months)) + " months to go"
    else:
      years = days / 365.0
      if  years <= 1:
          return "one year to go"
      else:
          return str(int(years)) + " years to go"





def formatSec(dt):

    delta = dt
    minutes = delta / MINUTE
    hours = delta / HOUR
    days = delta / DAY

    if delta <  0:
        return "??"

    if delta < 1 * MINUTE:    
      if delta == 1:
          return  "one second"
      else:
          return str(delta) + " seconds"


    if delta < 2 * MINUTE:
        return "a minute"


    if delta < 45 * MINUTE:
        return str(int(minutes)) + " minutes"

    if delta < 90 * MINUTE:
        return "one hour"

    if delta < 24 * HOUR:
        return str(int(hours)) + " hours"

    if delta < 48 * HOUR:
        return "a day"

    if delta < 30 * DAY:
        return str(int(days)) + " days"


    if delta < 12 * MONTH:
        months = delta / MONTH
        if months <= 1:
            return "one month"
        else:
            return str(int(months)) + " months"
    else:
      years = days / 365.0
      if  years <= 1:
          return "one year"
      else:
          return str(int(years)) + " years"


async def upnext(self,c,n,m):
    res = requests.get('https://radio.tildeverse.org/api/station/1/schedule')
    if res.status_code == 200:
        js = res.json()
        if len(js) < 1:
            await self.message(c,'[\x036radio\x0f] it appears that there is nothing on the schedule...')
            return
        up = js[0]
        await self.message(c,'[\x036radio\x0f] Up next: {}, {}!'.format(up['name'],timeDelta(up['start_timestamp'])))
    else:
        await self.message(c,'[\x036radio\x0f] something went wrong...')

async def nowplaying(self,c,n,m):
    res = requests.get("https://radio.tildeverse.org/api/nowplaying/1")
    if res.status_code == 200:
        js = res.json()
        if "station" not in js:
            await self.message(c,'[\x036radio\x0f] something went wrong...')
            return
        np = js['now_playing']
        #print(np)
        if np['streamer'] == "":
            await self.message(c,'[\x036radio\x0f] autodj has been playing {} for {} (next song in {})'.format(np['song']['text'],formatSec(np['elapsed']),formatSec(np['remaining']-1)))
        else:
            await self.message(c,'[\x036radio\x0f] {} has been playing "{}" for {} (next song in {}) ({} listeners!)'.format(np['streamer'],np['song']['text'],formatSec(np['elapsed']),formatSec(np['remaining']-1),js['listeners']['current']))
    else:
        await self.message(c,'[\x036radio\x0f] something went wrong...')



async def radioremind(self,c,n,m,scindex=0):
    res = requests.get('https://radio.tildeverse.org/api/station/1/schedule')
    if res.status_code == 200:
        js = res.json()
        if len(js) < scindex+1:
            await self.message(c,'[\x036radio\x0f] it appears that there is nothing on the schedule...')
            return
        up = js[scindex]

        dt = datetime.datetime.fromtimestamp(up['start_timestamp'])
        now = datetime.datetime.now()
        delta_time = (dt - now)
        delta_time = (delta_time.days * DAY + delta_time.seconds) - 30
        
        if delta_time < 1:
            await radioremind(self,c,n,m,scindex=scindex+1)
            return
        if len(m.strip()) > 0:
            toremind = m.strip()
        else:
            toremind = c

        if toremind in self.rreminders:
            await self.message(c,'[\x036radio\x0f] There is already a reminder set for {}, you can also specify somewhere else to send the reminder'.format(toremind))
            return
        await self.message(c,'[\x036radio\x0f] ok, il remind {} when its time for {}\'s show! (in {})'.format(toremind,up['name'],formatSec(delta_time)))
        
        task = asyncio.get_event_loop().create_task(remindTask(self, n, up, delta_time))
        self.rreminders[toremind] = task
        try:
            await task
        except asyncio.CancelledError:
            print('Reminder for {} cancelled'.format(toremind))
        finally:
            print('Reminder for {} finished'.format(toremind))
            self.rreminders.pop(toremind)
    else:
        await self.message(c,'[\x036radio\x0f] something went wrong...')

async def remindTask(self, n, up, delta_time):

    await asyncio.sleep(delta_time)
    await self.message(c,'[\x036radio\x0f] beep boop, {} is here to remind you that {}\'s show is coming up in about 30 seconds!'.format(n,up['name']))
 



async def init(self):
    self.rreminders = {}
    self.cmd['un'] = upnext
    self.cmd['upnext'] = upnext
    self.cmd['radioremind'] = radioremind
    self.help['radioremind'] = ['radioremind [where] - set a reminder that someone will stream','oh no i forgot what to put here!']
    self.help['upnext'] = ['upnext - get who will be up next on tilderadio\'s schedule','noice moosic']
    self.cmd['nowplaying'] = nowplaying
    self.help['nowplaying'] = ['nowplaying - when radiobot is dead use this instead!','lol']

