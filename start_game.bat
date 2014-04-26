@echo off

set /P ttrUsername="Username (DEFAULT: username): " || ^
set ttrUsername=username
set ttrPassword=password
set /P TTR_GAMESERVER="Client Agent IP (DEFAULT: 198.100.156.180): " || ^
set TTR_GAMESERVER=198.100.156.180

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

echo ===============================
echo Starting Toontown Infinite Retro...
echo ppython: %PPYTHON_PATH%
echo Username: %ttrUsername%
echo Client Agent IP: %TTR_GAMESERVER%
echo ===============================

%PPYTHON_PaTH% -m toontown.toonbase.ToontownStart
pause
