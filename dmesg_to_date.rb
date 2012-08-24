#!/usr/bin/env ruby

# Generates a fairly accurate timestamp of a dmesg event
#
# Tries to parse `uptime` output if /proc/uptime is unavailable


def uptime_in_seconds
  if ! File.readable?("/proc/uptime")
    return File.open("/proc/uptime", mode="r").gets[/^\d+/].to_i
  else 
    info = `uptime`.scan(/^\s(\d{2}.\d{2}.\d{2})\sup\s(\d+)\s(\w+),\s+(\d+)(:\d+|\w+)/).flatten!
    # => [["19:52:49", "48", "days", "1", ":26"]]

    now       = info[0]
    value     = info[1].to_i
    unit      = info[2].to_s
    precision = info[3].to_s
    surprise  = info[4].to_s

    seconds = 0

    case unit
    when "days"
      seconds = value*24*60*60
    when "hour"
      seconds = value*60*60
    when "min"
      seconds = value*60
    end

    if surprise.match(/^:(\d+)$/)[1]
      hours   = precision.to_i
      minutes = $1.to_i
      seconds += hours*60*60 + minutes*60
    elsif surprise.match(/min/)
      minutes = precision.to_i
      seconds += minutes*60
    end

    return seconds
  end
end

printf("System uptime in seconds: %d\n", uptime_in_seconds)

=begin
uptime = uptime_in_seconds
dmesg  = ARGV[0].match(/^(?:\[)?(\d+)/)[1].to_i
now    = Time.now
boot   = now - uptime
date   = boot + dmesg

puts "Now: #{now}" 
puts "Boot: #{boot}"
puts "Dmesg: #{date}"
=end
