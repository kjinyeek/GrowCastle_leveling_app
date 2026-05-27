@echo off
pyinstaller --onefile --noconsole --name GrowCastleCalculator main.py
xcopy /E /I /Y assets dist\assets
copy /Y settings.json dist\settings.json
echo.
echo Build complete. Upload dist\GrowCastleCalculator.exe and keep dist\assets + dist\settings.json with it if needed.
pause
