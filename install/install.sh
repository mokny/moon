#!/bin/bash
UUID=$(cat /proc/sys/kernel/random/uuid)
tmppath="/tmp/moon_${UUID}"
git clone https://github.com/mokny/tanks "${tmppath}"
mokka workspace create moon
mokka install moon ${tmppath}
rm -rf ${tmppath}