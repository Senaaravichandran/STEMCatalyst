@echo off
echo Starting STEM Problem Solver Backend...
echo.
echo Installing dependencies (if needed)...
call pip install -r requirements.txt
echo.
echo Starting Flask server...
echo Backend will be available at http://localhost:5000
echo.
call python app.py
