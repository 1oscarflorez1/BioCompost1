@echo off
REM ==========================================================
REM  BioCompost - Instalacion inicial (solo la primera vez en cada computador)
REM  Requisitos: Python 3.10+ y Docker Desktop abierto.
REM ==========================================================
title BioCompost - Instalacion
cd /d "%~dp0"

echo ==================================================
echo   BioCompost - Instalacion inicial
echo ==================================================
echo.

where py >nul 2>&1
if errorlevel 1 (
  echo [X] No se encontro Python. Instale Python 3.10 o superior desde https://www.python.org
  pause
  exit /b 1
)
py -3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)"
if errorlevel 1 (
  echo [X] Se necesita Python 3.10 o superior. Versiones instaladas:
  py -0
  pause
  exit /b 1
)

docker info >nul 2>&1
if errorlevel 1 (
  echo [X] Docker Desktop no esta abierto. Abralo y vuelva a ejecutar este archivo.
  pause
  exit /b 1
)

if not exist ".env" (
  copy ".env.example" ".env" >nul
  echo [OK] Se creo el archivo .env a partir de .env.example
)

if exist "backend\.venv\Scripts\python.exe" (
  backend\.venv\Scripts\python -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>&1
  if errorlevel 1 (
    echo [!] El entorno de Python existente usa una version antigua. Se va a recrear...
    rmdir /s /q backend\.venv
  )
)

if not exist "backend\.venv\Scripts\python.exe" (
  echo [1/4] Creando el entorno virtual de Python...
  py -3 -m venv backend\.venv
  if errorlevel 1 (
    echo [X] No se pudo crear el entorno virtual.
    pause
    exit /b 1
  )
)

echo [2/4] Instalando las librerias de Python (requiere internet)...
backend\.venv\Scripts\python -m pip install --upgrade pip -q
backend\.venv\Scripts\python -m pip install -r backend\requirements.txt -q
if errorlevel 1 (
  echo [X] Fallo la instalacion de librerias.
  pause
  exit /b 1
)

echo [3/4] Encendiendo Oracle en Docker (la primera vez descarga cerca de 1 GB)...
docker compose up -d
if errorlevel 1 (
  pause
  exit /b 1
)
call :esperar_oracle
if errorlevel 1 (
  pause
  exit /b 1
)

echo [4/4] Creando las tablas y cargando los datos de prueba...
pushd backend
.venv\Scripts\python init_db.py
set RESULTADO=%errorlevel%
popd
if not "%RESULTADO%"=="0" (
  pause
  exit /b 1
)

echo.
echo Instalacion terminada. Para usar el sistema ejecute iniciar.bat
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
if %INTENTOS% GEQ 120 (
  echo [X] Oracle no arranco a tiempo. Revise el contenedor en Docker Desktop.
  exit /b 1
)
ping -n 6 127.0.0.1 >nul
goto bucle_oracle
