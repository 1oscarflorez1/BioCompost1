@echo off
REM ==========================================================
REM  BioCompost - Enciende todo el sistema con doble clic:
REM  1) Oracle (Docker)  2) API FastAPI  3) Frontend  4) Navegador
REM ==========================================================
title BioCompost - Inicio
cd /d "%~dp0"

echo ==================================================
echo   BioCompost - Iniciando el sistema
echo ==================================================
echo.

if not exist ".env" (
  echo [X] Falta el archivo .env. Ejecute primero instalar.bat
  pause
  exit /b 1
)
if not exist "backend\.venv\Scripts\python.exe" (
  echo [X] Falta el entorno de Python. Ejecute primero instalar.bat
  pause
  exit /b 1
)
backend\.venv\Scripts\python -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>&1
if errorlevel 1 (
  echo [X] El entorno de Python del proyecto usa una version antigua.
  echo     Se necesita Python 3.10 o superior. Ejecute instalar.bat para repararlo.
  pause
  exit /b 1
)

docker info >nul 2>&1
if errorlevel 1 (
  echo [X] Docker Desktop no esta abierto.
  echo     Abralo, espere a que diga "Engine running" y vuelva a ejecutar este archivo.
  pause
  exit /b 1
)

echo [1/4] Encendiendo la base de datos Oracle en Docker...
docker compose up -d
if errorlevel 1 (
  pause
  exit /b 1
)
echo       Esperando a que Oracle este lista (puede tardar 1 o 2 minutos)...
call :esperar_oracle
if errorlevel 1 (
  pause
  exit /b 1
)

echo [2/4] Iniciando la API (FastAPI) en el puerto 8000...
netstat -ano | findstr ":8000 " | findstr "LISTENING" >nul
if errorlevel 1 (
  start "BioCompost API - NO CERRAR" /D "%~dp0backend" cmd /k .venv\Scripts\python -m uvicorn main:app
) else (
  echo       La API ya estaba en ejecucion.
)

echo [3/4] Iniciando el frontend en el puerto 5500...
netstat -ano | findstr ":5500 " | findstr "LISTENING" >nul
if errorlevel 1 (
  start "BioCompost Frontend - NO CERRAR" /D "%~dp0" cmd /k backend\.venv\Scripts\python -m http.server 5500 --directory frontend
) else (
  echo       El frontend ya estaba en ejecucion.
)

echo [4/4] Abriendo el navegador...
ping -n 5 127.0.0.1 >nul
start "" "http://127.0.0.1:8000/docs"
start "" "http://localhost:5500/login.html"

echo.
echo ==================================================
echo   Listo. Se abrieron dos ventanas negras:
echo   "BioCompost API" y "BioCompost Frontend".
echo   NO las cierre mientras use el sistema.
echo.
echo   Aplicacion: http://localhost:5500/login.html
echo   Swagger:    http://127.0.0.1:8000/docs
echo   Para apagar todo: detener.bat
echo ==================================================
pause
exit /b 0

:esperar_oracle
set /a INTENTOS=0
:bucle_oracle
set "ESTADO="
for /f "delims=" %%s in ('docker inspect -f "{{.State.Health.Status}}" biocompost-oracle 2^>nul') do set "ESTADO=%%s"
if "%ESTADO%"=="healthy" (
  echo       Oracle lista.
  exit /b 0
)
set /a INTENTOS+=1
if %INTENTOS% GEQ 72 (
  echo [X] Oracle no arranco a tiempo. Revise el contenedor en Docker Desktop.
  exit /b 1
)
ping -n 6 127.0.0.1 >nul
goto bucle_oracle
