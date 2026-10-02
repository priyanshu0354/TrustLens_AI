@echo off
echo =========================================
echo        TRUSTLENS AI - CODE SANGAM
echo =========================================
echo.
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)
call venv\Scripts\activate
echo Installing requirements...
python -m pip install -r requirements.txt
echo.
echo Starting TrustLens...
streamlit run app.py
pause
