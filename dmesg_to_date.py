#!/usr/bin/env python
import os
import re
import subprocess

def uptime_in_seconds():
    if not os.path.isfile("/proc/uptime"):
      uptime = 0
      with open("/proc/uptime") as f:
        for line in f:
          uptime = int(re.match('^\d+', line).group(0))
      return uptime
    else:
      info = re.split('^\s(\d{2}.\d{2}.\d{2})\sup\s(\d+)\s(\w+),\s+(\d+)(:\d+|\w+)', subprocess.check_output('uptime'))

      now       = info[1]
      value     = int(info[2])
      unit      = info[3]
      precision = info[4]
      surprise  = info[5]

      seconds = 0

      if unit == "days":
        seconds = value*24*60*60
      elif unit == "hour":
        seconds = value*60*60
      elif unit == "min":
        seconds = value*60

      # There has to be a better way to do this
      m = re.match('^:(\d+)$', surprise)
      if m:
        hours   = int(precision)
        minutes = int(m.group(1))
        seconds += hours*60*60 + minutes*60
      else:
        m = re.match('min', surprise)
        if m:
          minutes = int(precision)
          seconds += minutes*60

      return seconds

print 'System uptime in seconds: %d' % uptime_in_seconds()
