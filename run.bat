@echo off
cd /d "%~dp0"
flet run --web --port 8000 main.py
pause
