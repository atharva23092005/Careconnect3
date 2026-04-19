@echo off
echo ========================================
echo CareConnect - Fresh Start
echo ========================================
echo.

echo [1/3] Stopping any running Python processes...
taskkill /F /IM python.exe >nul 2>&1
timeout /t 2 /nobreak >nul
echo Done.

echo.
echo [2/3] Clearing old database...
if exist careconnect.db (
    del careconnect.db
    echo Old database deleted.
) else (
    echo No old database found.
)

echo.
echo [3/3] Starting fresh application...
echo.
echo ========================================
echo IMPORTANT: Clear your browser cookies!
echo ========================================
echo.
echo In your browser:
echo 1. Press Ctrl+Shift+Delete
echo 2. Clear cookies for the last hour
echo 3. Or use Incognito/Private mode
echo.
echo Then go to: http://127.0.0.1:5000
echo.
echo Login: admin / admin123
echo.
echo ========================================
echo.

python app_fixed.py
