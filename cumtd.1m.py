#!/usr/bin/env -S PATH="${PATH}:/Users/${USER}/miniconda3/bin/" LC_ALL=en_US.UTF-8 python3
# -*- coding: utf-8 -*-

# <bitbar.title>CUMTD Bus Tracker</bitbar.title>
# <bitbar.version>v2.0</bitbar.version>
# <bitbar.author>bcongdon</bitbar.author>
# <bitbar.author.github>bcongdon</bitbar.author.github>
# <bitbar.desc>Displays upcoming bus departure for the CUMTD bus system</bitbar.desc>
# <bitbar.dependencies>python</bitbar.dependencies>

import requests
import pytz
from pytz import timezone
from datetime import datetime
import json
import time
import sys
import codecs

# Set this to your CUMTD API key
API_KEY = ''

# Set this to the CUMTD stop you want to monitor
# You can find the stop ID from https://mtd.org/
STOP_TO_MONITOR = ''

# Don't change anything below this line.
# --------------------------------------
API_URL = 'https://developer.cumtd.com/api/v2.2/json/getdeparturesbystop'
INFO_URL = 'https://mtd.org/maps-and-schedules/bus-stops/info/'

r = requests.get(API_URL, params=dict(key=API_KEY, stop_id=STOP_TO_MONITOR))
data = r.json()

departures = data.get('departures', [])

output = '🚌\n---\n'

for departure in departures:
    params = 'href={}'.format(INFO_URL + STOP_TO_MONITOR)
    output += '{}: {} min |{}\n'.format(departure['headsign'],
                                        departure['expected_mins'],
                                        params)

print(output)
