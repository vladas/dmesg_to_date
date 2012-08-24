#!/usr/bin/env python
# coding=utf8
import os
import re
import string
import subprocess

def uptime_in_seconds():
    if os.path.isfile("/proc/uptime"):
      uptime = 0
      with open("/proc/uptime") as f:
        for line in f:
          uptime = int(re.match('^\d+', line).group(0))
      return uptime
    else:
      return uptime_cmd_to_seconds(subprocess.check_output('uptime'))

def uptime_cmd_to_seconds(uptime):

  seconds = 0
  info = re.split('^.+up\s(.+),\s+\d+\susers', uptime)[1].split(',') # split into chunks

  for time in info:
    time = time.strip()
    if re.search('(\d+)\:(\d+)', time): # match time, eg. 21:41
      m = re.search('(\d+)\:(\d+)', time)
      seconds += int(m.group(1)) * 60 * 60 # hours
      seconds += int(m.group(2)) * 60 # mins
    elif re.search('(\d+)\s+(\w+)', time): # match over units, eg. 2 days, 5 min
      m = re.search('(\d+)\s+(\w+)', time)
      value     = int(m.group(1))
      unit      = m.group(2)
      
      if unit == "days":
        seconds += value*24*60*60
      elif unit == "hour":
        seconds += value*60*60
      elif unit == "min":
        seconds += value*60
      
  return seconds
  
''' OS X '''
#print uptime_cmd_to_seconds('19:16  up 2 days, 21:41, 3 users, load averages: 3.01 2.60 1.93')
''' Ubuntu '''
#print uptime_cmd_to_seconds('﻿ 19:11:47 up 5 min,  2 users,  load average: 2.29, 2.14, 1.04')
print 'System uptime in seconds: %d' % uptime_in_seconds()