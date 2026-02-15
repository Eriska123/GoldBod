@echo off
REM ======================================
echo Starting GoldBod3 Data Pipeline
echo ======================================
echo.

REM ---- Run GoldBod3 Python Script ----
python goldbod3.py

IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: goldbod3.py failed to execute.
    pause
    exit /b 1
)

echo.
echo ======================================
echo GoldBod3 pipeline completed successfully!
echo ======================================
echo.
pause
