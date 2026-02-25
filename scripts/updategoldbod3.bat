@echo off

echo ======================================
echo Starting GoldBod3 Data Pipeline
echo ======================================
echo.

REM -------------------------------------------------
REM Get the folder where this .bat file is located
REM -------------------------------------------------
set SCRIPT_DIR=%~dp0

REM Move from scripts\ to project root
cd /d "%SCRIPT_DIR%\.."

echo Project root:
cd
echo.

REM -------------------------------------------------
REM Run ingestion
REM -------------------------------------------------
echo Running ingestion...
python ingestion\goldbod3.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: goldbod3.py failed to execute.
    pause
    exit /b
)

echo.
echo Ingestion successful.

REM -------------------------------------------------
REM Launch Streamlit
REM -------------------------------------------------
echo Launching dashboard...
streamlit run streamlit\goldbod3_dashboard1.py

pause