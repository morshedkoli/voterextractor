@echo off
echo Starting Bengali Voter Data Extractor...
echo.

REM Start backend in new window
echo Starting Backend Server...
start "Backend API" cmd /k "cd /d %~dp0 && python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload"

REM Wait 3 seconds for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend in new window
echo Starting Frontend Server...
start "Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

REM Wait 5 seconds for frontend to start
timeout /t 5 /nobreak >nul

REM Open browser
echo Opening browser...
start http://localhost:3000

echo.
echo Application started successfully!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to exit this window...
pause >nul
