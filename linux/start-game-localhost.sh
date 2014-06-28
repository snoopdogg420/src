#!/bin/sh
cd ..

# Read the contents of PPYTHON_PATH into $PPYTHON_PATH:
PPYTHON_PATH=`cat PPYTHON_PATH`

# Get the user input:
read -p "Username: " ttiUsername

# Export the environment variables:
export ttiUsername=$ttiUsername
export ttiPassword="password"
export TTI_PLAYCOOKIE=$ttiUsername
export TTI_GAMESERVER="127.0.0.1"

echo "==============================="
echo "Starting Toontown Infinite..."
echo "ppython: $PPYTHON_PATH"
echo "Username: $ttiUsername"
echo "Gameserver: $TTI_GAMESERVER"
echo "==============================="

$PPYTHON_PATH -m toontown.toonbase.ClientStart
