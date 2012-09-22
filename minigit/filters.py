from minigit import app
from datetime import *
from dateutil import relativedelta
from flask import Markup
import time, os

# format a timestamp in default format (0000-00-00 00:00:00)
@app.template_filter()
def formattime(s):
    return s.strftime("%Y-%m-%d %H:%M:%S")

@app.template_filter()
def nicedate(s):
    return s.strftime("%B %d, %Y")

def _s(n, s):
    if n == 0:
        return ""
    return str(n) + " " + s + ("s" if n > 1 else "")

def _delta(delta):
    short = True
    threshold = 2
    if delta.years > 0:
        return _s(delta.years, "year") + ("" if short and delta.years > threshold else " " + _s(delta.months, "month"))
    if delta.months > 0:
        return _s(delta.months, "month") + ("" if short and delta.months > threshold else " " + _s(delta.days, "day"))
    if delta.days > 0:
        return _s(delta.days, "day") + ("" if short and delta.days > threshold else " " + _s(delta.hours, "hour"))
    if delta.hours > 0:
        return _s(delta.hours, "hour") + ("" if short and delta.hours > threshold else " " + _s(delta.minutes, "minute"))
    if delta.minutes > 0:
        return _s(delta.minutes, "minute") + ("" if short and delta.minutes > threshold else " " + _s(delta.seconds, "second"))
    return _s(delta.seconds, "second")

def timedelta(starttime, endtime):
    return relativedelta.relativedelta(starttime, endtime)

def _absdelta(d):
    if d.seconds < 0 or d.minutes < 0 or d.hours < 0 or d.days < 0 or d.months < 0 or d.years < 0:
        return -d
    return d

# format a timedelta in human-readable format (e.g. "in 20 minutes" or "3 weeks ago")
@app.template_filter()
def humandelta(s, other = None):
    if other:
        # we got 2 datetimes
        return _delta(_absdelta(timedelta(other, s))).strip()


    if s.seconds < 0 or s.minutes < 0 or s.hours < 0 or s.days < 0 or s.months < 0 or s.years < 0:
        return "%s ago" % _delta(-s).strip()
    elif s.seconds > 0 or s.minutes > 0 or s.hours > 0 or s.days > 0 or s.months > 0 or s.years > 0:
        return "in %s" % _delta(s).strip()
    else:
        return s

@app.template_filter()
def humantime(s):
    diff = timedelta(s, datetime.utcnow())
    if diff.years < 1:
        return Markup('<span title="' + formattime(s) + '" class="time-title">' + humandelta(diff) + '</span>')
    else:
        return formattime(s)


@app.template_filter()
def epoch(s):
    # s = datetime.utcnow()
    return time.mktime(s.timetuple())

@app.template_filter()
def is_string(o):
    return type(o) == str

@app.template_filter()
def pathsplit(o):
    p = os.path.split(o)
    while len(p) > 0 and p[0] == "": p = p[1:]
    while len(p) > 0 and p[-1] == "": p = p[:-1]
    return p

