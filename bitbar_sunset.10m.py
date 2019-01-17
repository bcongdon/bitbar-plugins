#!/usr/bin/env -S PATH="${PATH}:/Users/${USER}/miniconda3/bin/" LC_ALL=en_US.UTF-8 python3
# -*- coding: utf-8 -*-

# <bitbar.title>Sunset Time</bitbar.title>
# <bitbar.version>v2.0</bitbar.version>
# <bitbar.author>bcongdon</bitbar.author>
# <bitbar.author.github>bcongdon</bitbar.author.github>
# <bitbar.desc>Displays the sunset time in your current location</bitbar.desc>
# <bitbar.dependencies>python</bitbar.dependencies>

import urllib.request
import pytz
from pytz import timezone
from datetime import datetime
import json
import time
import sys
import codecs

ip_url = "http://ip-api.com/json"


def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(
        now_timestamp
    )
    return utc_datetime + offset


def parse_utc_timestamp(utc_timestamp):
    date, tzoffset = utc_timestamp.split("+")
    # Python doesn't support colons in the tz offset
    tzoffset = tzoffset.replace(":", "")
    parsed_date = datetime.strptime(
        "{}+{}".format(date, tzoffset), "%Y-%m-%dT%H:%M:%S%z"
    )
    return parsed_date


try:
    r = urllib.request.urlopen(ip_url).read()
except IOError as e:
    raise("Unable to get location")

payload = json.loads(r)
lat, lon = payload.get("lat"), payload.get("lon")

current_date = datetime.now().date().isoformat()
sun_api_url = "https://api.sunrise-sunset.org/json?lat={}&lng={}&date={}&formatted=0".format(
    lat, lon, current_date
)

try:
    response = urllib.request.urlopen(sun_api_url).read()
except IOError as e:
    raise("Unable to contact Sunset API")

payload = json.loads(response)
if payload.get("status") != "OK":
    raise("Got bad response from API")

sunset = parse_utc_timestamp(payload.get("results").get("sunset"))
sunset_str = datetime_from_utc_to_local(sunset).strftime("%I:%M%p")
if sunset_str.startswith("0"):
    sunset_str = sunset_str[1:]

now = pytz.utc.localize(datetime.utcnow())
until_sunset = sunset - now
hours = until_sunset.seconds / 3600

# Only display if sunset is within the next 2 hours or has passed in last ~1 hour
if (now < sunset and abs(24 - hours) <= 2) or abs(24 - hours) <= 1:
    print(u"🌅 {}".format(sunset_str))
