@echo off

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

set /P ttiUsername="Username: "
set /P ttiPassword="Password: "
set /P TTI_GAMESERVER="Gameserver (DEFAULT: 192.99.200.107): " || ^
set TTI_GAMESERVER=192.99.200.107

echo ===============================
echo Starting Toontown Infinite...
echo ppython: %PPYTHON_PATH%
echo Username: %ttiUsername%
echo Password: %ttiPassword%
echo Gameserver: %TTI_GAMESERVER%
echo ===============================

%PPYTHON_PATH% -m toontown.toonbase.ClientStartRemoteDB
pause
