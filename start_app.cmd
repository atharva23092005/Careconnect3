@echo off
echo ========================================
echo Starting CareConnect Application
echo ========================================
echo.

echo Checking if model exists...
if not exist model.pkl (
    echo Model not found! Training model...
    python train_model.py
    if errorlevel 1 (
        echo ERROR: Model training failed!
        echo Please run: python train_model.py
        pause
        exit /b 1
    )
)

echo.
echo Starting Flask application...
echo Open your browser to: http://127.0.0.1:5000
echo.
echo Login credentials:
echo   Username: admin
echo   Password: admin123
echo.
echo Press Ctrl+C to stop the server
echo.

python app_fixed.py
