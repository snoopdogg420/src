@echo off
python.exe -m toontown.uberdog.ServiceStart --base-channel 1000000 --max-channels 1000000 --stateserver 10000 --astron-ip "127.0.0.1:7199" --eventlogger-ip "127.0.0.1:7197"
pause