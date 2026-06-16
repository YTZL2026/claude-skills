@echo off
title Disk Fix

echo === Step 1/3: Bring disk online and assign letter F ===
(
echo select disk 1
echo online disk
echo attributes disk clear readonly
echo select partition 1
echo assign letter=F
echo exit
) > %TEMP%\fix_disk.txt
diskpart /s %TEMP%\fix_disk.txt

echo.
echo === Step 2/3: Change SAN policy to OnlineAll ===
(
echo SAN POLICY=OnlineAll
echo exit
) > %TEMP%\fix_san.txt
diskpart /s %TEMP%\fix_san.txt

echo.
echo === Step 3/3: Disable USB selective suspend ===
powercfg /SETACVALUEINDEX SCHEME_CURRENT 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53c8e1a2a1a2 0
powercfg /SETDCVALUEINDEX SCHEME_CURRENT 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53c8e1a2a1a2 0
powercfg /S SCHEME_CURRENT

echo.
echo === DONE ===
echo Drive F: should now be accessible.
echo SAN policy set to OnlineAll - disk will auto-mount on reconnect.
echo.
pause
del %TEMP%\fix_disk.txt %TEMP%\fix_san.txt 2>nul
