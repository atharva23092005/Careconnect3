@echo off
echo ========================================
echo CareConnect Production Setup
echo ========================================
echo.

echo [1/5] Training ML Model...
python train_model.py
if errorlevel 1 (
    echo ERROR: Model training failed!
    pause
    exit /b 1
)
echo.

echo [2/5] Initializing Database...
python init_db.py
if errorlevel 1 (
    echo ERROR: Database initialization failed!
    pause
    exit /b 1
)
echo.

echo [3/5] Generating Secret Key...
echo Your SECRET_KEY for deployment:
python -c "import secrets; print(secrets.token_hex(32))"
echo.
echo IMPORTANT: Copy this key and save it for deployment!
echo.

echo [4/5] Testing Application...
echo Starting test server on http://127.0.0.1:5000
echo Press Ctrl+C to stop when done testing
echo.
python app_production.py
echo.

echo [5/5] Ready for Deployment!
echo.
echo Next steps:
echo 1. Commit all changes: git add . ^&^& git commit -m "Production ready" ^&^& git push
echo 2. Follow DEPLOYMENT_GUIDE.md for Render/Railway deployment
echo 3. Set SECRET_KEY environment variable with the key shown above
echo.
pause
