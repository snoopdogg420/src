@echo off
cd ../

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

set MAX_CHANNELS=999999
set STATESERVER=4002
set ASTRON_IP=127.0.0.1:7199
set EVENTLOGGER_IP=127.0.0.1:7197
set /P DISTRICT_NAME="District Name (DEFAULT: Retroville): " || ^
set DISTRICT_NAME=Retroville
set /P BASE_CHANNEL="Base Channel (DEFAULT: 401000000): " || ^
set BASE_CHANNEL=401000000

echo ===============================
echo Starting Toontown Infinite AI server...
echo ppython: %PPYTHON_PATH%
echo District name: %DISTRICT_NAME%
echo Base channel: %BASE_CHANNEL%
echo Max channels: %MAX_CHANNELS%
echo State Server: %STATESERVER%
echo Astron IP: %ASTRON_IP%
echo Event Logger IP: %EVENTLOGGER_IP%
echo ===============================

:main
%PPYTHON_PATH% -m toontown.ai.ServiceStart --base-channel %BASE_CHANNEL% ^
               --max-channels %MAX_CHANNELS% --stateserver %STATESERVER% ^
               --astron-ip %ASTRON_IP% --eventlogger-ip %EVENTLOGGER_IP% ^
               --district-name "%DISTRICT_NAME%"

goto main
