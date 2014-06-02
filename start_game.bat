@echo off

set /P ttiUsername="Username: "
set /P ttiPassword="Password: "
set /P TTI_GAMESERVER="Client Agent IP (DEFAULT: 192.99.21.164): " || ^
set TTI_GAMESERVER=192.99.21.164

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

echo ===============================
echo Starting Toontown Infinite Retro...
echo ppython: %PPYTHON_PATH%
echo Username: %ttiUsername%
echo Client Agent IP: %TTI_GAMESERVER%
echo ===============================

%PPYTHON_PATH% -m toontown.toonbase.ToontownStartRemote
pause
