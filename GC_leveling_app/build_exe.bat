@echo off
pip install pyinstaller
pyinstaller --onefile --noconsole --name GrowCastleCalculator main.py
pause
