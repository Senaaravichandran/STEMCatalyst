@echo off
title STEM Problem Solver - Full Stack Application
color 0A

echo ====================================================
echo         STEM Problem Solver - Full Stack App
echo ====================================================
echo.
echo This script will start both frontend and backend servers
echo.
echo Requirements:
echo - Node.js (for React frontend)
echo - Python 3.8+ (for Flask backend)
echo - Internet connection (for Mistral AI API)
echo.
echo ====================================================
echo.

pause

echo Starting Backend Server...
echo.
start cmd /k "cd /d backend && start.bat"

timeout /t 3 /nobreak >nul

echo Starting Frontend Server...
echo.
start cmd /k "cd /d frontend && start.bat"

echo.
echo ====================================================
echo Both servers are starting in separate windows:
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Wait for both servers to fully start, then open:
echo http://localhost:3000 in your browser
echo.
echo Press any key to exit this launcher...
echo ====================================================
pause >nul
