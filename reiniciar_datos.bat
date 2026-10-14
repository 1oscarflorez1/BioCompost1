@echo off
REM ==========================================================
REM  BioCompost - Vuelve a dejar la base de datos con los datos de prueba
REM  originales (borra lo que se haya agregado en los ensayos).
REM  Usar antes de la presentacion. Oracle debe estar encendida.
REM ==========================================================
title BioCompost - Reiniciar datos
cd /d "%~dp0backend"

echo Esto BORRA todo lo registrado y vuelve a cargar los datos de prueba.
choice /C SN /M "Desea continuar"
if errorlevel 2 exit /b 0

.venv\Scripts\python init_db.py
pause
