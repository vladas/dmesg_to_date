#!/usr/bin/php
<?php
function uptime_in_seconds()
{
    if (is_readable("/proc/uptime")) {
        // parse ﻿778.53 from ﻿778.53 500.11
        $uptimeArr = explode(' ', file_get_contents('/proc/uptime'));
        return (int) $uptimeArr[0];
    } else {
        return uptime_cmd_to_seconds(`uptime`);
    }
}

function uptime_cmd_to_seconds($uptime)
{
    $seconds = 0;
    $matches = array();
    if (preg_match('/^.+up\s(.+),\s+\d+\susers/', $uptime, $matches)) {
        $timeArr = explode(',', $matches[1]);
        foreach ($timeArr as $timeStr) {
            $timeStr = trim($timeStr);
            if (preg_match('/(\d+)\:(\d+)/', $timeStr, $matches)) {
                $seconds += (int) $matches[1] * 60 * 60; # hours
                $seconds += (int) $matches[2] * 60; # mins
            } elseif (preg_match('/(\d+)\s+(\w+)/', $timeStr, $matches)) {
                $value = (int) $matches[1];
                $unit = (int) $matches[2];
                if ($unit == "days") {
                    $seconds += $value * 24 * 60 * 60;
                } elseif ($unit == "hour") {
                    $seconds += $value * 60 * 60;
                } elseif ($unit == "min") {
                    $seconds += $value * 60;
                }
            }
        }
    }
    return $seconds;
}
echo 'System uptime in seconds: ', (int) uptime_in_seconds(), "\n";

// OS X
//echo uptime_cmd_to_seconds('19:16  up 2 days, 21:41, 3 users, load averages: 3.01 2.60 1.93'), "\n";
// Ubuntu
//echo uptime_cmd_to_seconds('﻿ 19:11:47 up 5 min,  2 users,  load average: 2.29, 2.14, 1.04'), "\n";
