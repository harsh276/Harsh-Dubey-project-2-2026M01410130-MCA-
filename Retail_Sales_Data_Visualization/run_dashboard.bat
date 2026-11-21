@echo off
title Retail Sales Analytics Dashboard
echo ===================================================
echo Starting Retail Sales Analytics Web Dashboard...
echo ===================================================
cd /d "%~dp0"
python -m streamlit run app.py
pause
