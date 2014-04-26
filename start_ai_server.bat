@echo off
python.exe -m toontown.ai.ServiceStart --base-channel 40100000 --max-channels 99999999 --stateserver 10000 --district-name "Retroville" --astron-ip "127.0.0.1:7199" --eventlogger-ip "127.0.0.1:7196"
pause