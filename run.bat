@echo off
echo ===================================================
echo Starting Helmet Detection Application (MP_deployment)
echo ===================================================
echo.

:: Get the directory where the batch file is located
set APP_DIR=%~dp0
cd /d "%APP_DIR%"

:: Start the Python backend in a new command window
echo [1/3] Starting FastAPI Backend...
start "Backend Server" cmd /k "cd /d ""%APP_DIR%"" && python -m backend.main"

:: Start the Vite frontend in a new command window
echo [2/3] Starting React Frontend...
start "Frontend Server" cmd /k "cd /d ""%APP_DIR%frontend"" && npm run dev"

:: Start Cloudflare Tunnel (Using project-specific tunnel_config.yml)
echo [3/3] Starting Cloudflare Tunnel...
start "Cloudflare Tunnel" cmd /k "cloudflared tunnel --config tunnel_config.yml run"

echo.
echo ✅ Start scripts initiated!
echo ---------------------------------------------------
echo Three new terminal windows should open:
echo 1. Backend Server (usually runs on http://localhost:8000/docs)
echo 2. Frontend Server (usually runs on http://localhost:5173)
echo 3. Cloudflare Tunnel (proxying to localhost:8000)
echo ---------------------------------------------------
echo Keep those windows open to keep the application running.
echo To stop the application, simply close the generated windows.
echo ===================================================
pause
