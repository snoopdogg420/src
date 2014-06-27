#!/bin/sh
cd ..

# Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
PPYTHON_PATH=`cat PPYTHON_PATH`

# set /P ttiUsername="Username (DEFAULT: username): " || ^
# set ttiUsername=username
# set ttiPassword=password
# set TTI_PLAYCOOKIE=%ttiUsername%
# set /P TTI_GAMESERVER="Gameserver (DEFAULT: 192.99.200.107): " || ^
# set TTI_GAMESERVER=192.99.200.107

# echo ===============================
# echo Starting Toontown Infinite...
# echo ppython: %PPYTHON_PATH%
# echo Username: %ttiUsername%
# echo Gameserver: %TTI_GAMESERVER%
# echo ===============================

# %PPYTHON_PATH% -m toontown.toonbase.ClientStart
# pause
