#!/usr/bin/env -S PATH="${PATH}:/Users/${USER}/miniconda3/bin/" LC_ALL=en_US.UTF-8 python3
# -*- coding: utf-8 -*-

# <bitbar.title>Sunset Time</bitbar.title>
# <bitbar.version>v2.0</bitbar.version>
# <bitbar.author>bcongdon</bitbar.author>
# <bitbar.author.github>bcongdon</bitbar.author.github>
# <bitbar.desc>Displays the sunset time in your current location</bitbar.desc>
# <bitbar.dependencies>python</bitbar.dependencies>

import urllib.request
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
    return datetime.strptime("{}+{}".format(date, tzoffset), "%Y-%m-%dT%H:%M:%S%z")


try:
    r = urllib.request.urlopen(ip_url).read()
except IOError as e:
    print("Unable to get location")
    exit(1)

payload = json.loads(r)
lat, lon = payload.get("lat"), payload.get("lon")

sun_api_url = "https://api.sunrise-sunset.org/json?lat={}&lng={}&formatted=0".format(
    lat, lon
)

try:
    response = urllib.request.urlopen(sun_api_url).read()
except IOError as e:
    print("Unable to contact Sunset API")
    exit(1)

payload = json.loads(response)
if payload.get("status") != "OK":
    print("Got bad response from API")
    exit(1)

sunset = parse_utc_timestamp(payload.get("results").get("sunset"))
sunset_str = datetime_from_utc_to_local(sunset).strftime("%I:%M%p")
if sunset_str.startswith("0"):
    sunset_str = sunset_str[1:]
print(u"🌅 {}".format(sunset_str))
