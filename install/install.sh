#!/bin/bash
# Install with curl -sSL https://raw.githubusercontent.com/mokny/moon/main/install/install.sh | bash
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
git clone https://github.com/mokny/moon "${tmppath}"
mokka workspace create ${workspace}
mokka install ${workspace} ${tmppath}

echo "Running setup for project folder..."

cp -rf ${tmppath}/custom ${project}

echo "Removing temporary files..."
rm -rf ${tmppath}


#mokka run ${workspace} moon setup ${project} 
#sleep 2
#mokka kill ${workspace} moon

echo "Setting options..."
mokka setopt ${workspace} moon root ${project} 
mokka setopt ${workspace} moon httpdocs ${project}/www

echo "Running moon..."
mokka run ${workspace} moon

echo "Your Project Directory: ${project}"
echo "To kill Moon: mokka kill ${workspace} moon"
echo "To (re)start Moon: mokka run ${workspace} moon"