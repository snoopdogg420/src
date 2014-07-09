#!/bin/bash
cd ..

# Get the user input:
read -p "Username: " ttiUsername
read -s -p "Password: " ttiPassword
echo
read -p "Gameserver (DEFAULT: 192.99.200.107): " TTI_GAMESERVER
TTI_GAMESERVER=${TTI_GAMESERVER:-"192.99.200.107"}

# Export the environment variables:
export ttiUsername=$ttiUsername
export ttiPassword=$ttiPassword
export TTI_PLAYCOOKIE=$ttiUsername
export TTI_GAMESERVER=$TTI_GAMESERVER

echo "==============================="
echo "Starting Toontown Infinite..."
echo "Username: $ttiUsername"
echo "Gameserver: $TTI_GAMESERVER"
echo "==============================="

/usr/bin/python2 -m toontown.toonbase.ClientStartRemoteDB
