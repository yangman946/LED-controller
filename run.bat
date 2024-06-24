echo off

cd C:\Users\Clarence\Documents\GitHub\LED-controller

start /B python Main.py

cd C:\Users\Clarence\Documents\GitHub\LED-controller\audio
start /B python visualizer.py

rem Wait for the user to close the batch program
pause

rem Terminate the Python processes
taskkill /F /IM python.exe /T