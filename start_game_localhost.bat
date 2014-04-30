@echo off

set /P tti-rUsername="Username (DEFAULT: username): " || ^
set tti-rUsername=username
set tti-rPassword=password
set TTI-R_PLAYCOOKIE=%tti-rUsername%
set TTI-R_GAMESERVER=127.0.0.1

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

echo ===============================
echo Starting Toontown Infinite Retro...
echo ppython: %PPYTHON_PATH%
echo Username: %tti-rUsername%
echo Client Agent IP: %TTI-R_GAMESERVER%
echo ===============================

%PPYTHON_PaTH% -m toontown.toonbase.ToontownStart
pause
