@echo off
REM ==========================================================
REM  BioCompost - Consola SQL de Oracle (SQL*Plus dentro de Docker)
REM  Abre una consola conectada a la base del proyecto para ver las
REM  tablas y ejecutar consultas SQL. Oracle debe estar encendida.
REM ==========================================================
title BioCompost - Consola Oracle
cd /d "%~dp0"

docker info >nul 2>&1
if errorlevel 1 (
  echo [X] Docker Desktop no esta abierto.
  pause
  exit /b 1
)

set "ESTADO="
for /f "delims=" %%s in ('docker inspect -f "{{.State.Health.Status}}" biocompost-oracle 2^>nul') do set "ESTADO=%%s"
if not "%ESTADO%"=="healthy" (
  echo [X] Oracle no esta encendida. Ejecute primero iniciar.bat
  pause
  exit /b 1
)

REM Usuario y contrasena de la base, leidos del archivo .env
for /f "usebackq tokens=1,* delims==" %%a in (".env") do (
  if "%%a"=="DB_USER" set "DB_USER=%%b"
  if "%%a"=="DB_PASSWORD" set "DB_PASSWORD=%%b"
)

REM Copia el archivo de formato al contenedor y abre SQL*Plus
docker exec biocompost-oracle mkdir -p /tmp/biocompost
docker exec -i biocompost-oracle bash -c "tr -d '\r' > /tmp/biocompost/consola.sql" < "database\consola.sql"
docker exec -it biocompost-oracle sqlplus -L "%DB_USER%/%DB_PASSWORD%@//localhost/FREEPDB1" @/tmp/biocompost/consola.sql
pause
