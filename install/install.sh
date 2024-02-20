#!/bin/bash
# Install with curl -sSL https://raw.githubusercontent.com/mokny/tanks/main/install/install.sh | bash
echo " ______                    _ "
echo "|  ___ \                  | |"
echo "| | _ | | ___   ___  ____ | |"
echo "| || || |/ _ \ / _ \|  _ \|_|"
echo "| || || | |_| | |_| | | | |_ "
echo "|_||_||_|\___/ \___/|_| |_|_|"

echo "Website: https://github.com/mokny/moon"


read -p "Enter Workspace-Ident: " workspace </dev/tty
read -p "Absolute project directory: " project </dev/tty

UUID=$(cat /proc/sys/kernel/random/uuid)
tmppath="/tmp/moon_${UUID}"
git clone https://github.com/mokny/tanks "${tmppath}"
mokka workspace create ${workspace}
mokka install ${workspace} ${tmppath}
rm -rf ${tmppath}

echo "Running setup for project folder..."

mokka run ${workspace} moon setup ${project} 
sleep 2
mokka kill ${workspace} moon

mokka run ${workspace} moon