@echo off

call venv\scripts\activate
venv\scripts\pyinstaller --add-data assets;assets ^
            --add-data venv\Lib\site-packages\wsdl;wsdl ^
            --icon "assets\favicon.ico" ^
            --name "Camera Controller" ^
            --noconsole ^
            --clean ^
            --windowed ^
            --log-level DEBUG ^
            controls.py

rem copy "dist\Camera Controller.exe" "G:\Shared drives\Z-BSL-RADARIQ-SharedFiles\Production\Release\Controller"

rem RMDIR /Q/S dist
RMDIR /Q/S build
rm "Camera Controller.spec"


echo Build completed.
pause