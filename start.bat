@echo off
title PROJECTVERSE Server
cd /d "%~dp0"
echo Starting PROJECTVERSE Server on http://localhost:8000 ...
python server.py
pause
