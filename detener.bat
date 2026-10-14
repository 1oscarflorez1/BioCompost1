@echo off
REM ==========================================================
REM  BioCompost - Apaga la API, el frontend y la base de datos
REM ==========================================================
title BioCompost - Detener
cd /d "%~dp0"

echo Cerrando la API (puerto 8000) y el frontend (puerto 5500)...
for /f "tokens=5" %%p in ('netstat -ano ^| findstr ":8000 " ^| findstr "LISTENING"') do taskkill /PID %%p /T /F >nul 2>&1
for /f "tokens=5" %%p in ('netstat -ano ^| findstr ":5500 " ^| findstr "LISTENING"') do taskkill /PID %%p /T /F >nul 2>&1

echo Deteniendo la base de datos Oracle (los datos se conservan)...
docker compose stop

echo.
echo Sistema detenido. Ya puede cerrar las ventanas "BioCompost".
echo Para volver a encenderlo: iniciar.bat
pause
