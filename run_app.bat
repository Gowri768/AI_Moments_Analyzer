@echo off
title AI Moments Analyzer Web App
echo ==========================================
echo Starting AI Moments Analyzer Web App...
echo ==========================================
echo.
echo Please wait while the AI models load. This may take 15-30 seconds.
echo A browser window will open automatically.
echo.

:: Launch the browser after a 5 second delay to give the server time to start
start "" cmd /c "timeout /t 5 >nul && start http://127.0.0.1:8000"

:: Start the FastAPI server
python -m uvicorn app:app --port 8000

echo.
pause
