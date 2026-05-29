@echo off
setlocal

REM Clean previous builds so old files do not confuse the new exe.
rmdir /S /Q build 2>nul
rmdir /S /Q dist 2>nul
del /Q GrowCastleCalculator.spec 2>nul

REM Build a true one-file exe with images bundled inside the exe.
pyinstaller --onefile --noconsole --name GrowCastleCalculator --add-data "assets;assets" main.py

echo.
echo Build complete.
echo New exe: dist\GrowCastleCalculator.exe
echo You can upload this exe alone to GitHub Releases.
pause
