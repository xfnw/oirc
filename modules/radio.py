
import requests


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

async def init(self):
    self.cmd['un'] = upnext
    self.cmd['upnext'] = upnext
    self.help['upnext'] = ['upnext - get who will be up next on tilderadio\'s schedule','noice moosic']


