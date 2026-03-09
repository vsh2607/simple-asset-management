@echo off
setlocal EnableExtensions EnableDelayedExpansion

echo =====================================
echo   Manajemen Asset BNNK Sleman
echo   Update index.html dari GitHub
echo =====================================
echo.

REM You can pass raw URL as argument:
REM UPDATE_INDEX.bat https://raw.githubusercontent.com/USERNAME/REPO/main/index.html
set "RAW_URL=%~1"
if "%RAW_URL%"=="" set "RAW_URL=https://github.com/vsh2607/simple-asset-management/blob/main/index.html"
set "DL_URL=%RAW_URL%"
set "DL_URL=%DL_URL:https://github.com/=https://raw.githubusercontent.com/%"
set "DL_URL=%DL_URL:/blob/=/%"

set "BASE_DIR=%~dp0"
set "TARGET=%BASE_DIR%index.html"
set "BACKUP=%BASE_DIR%index.backup.html"
set "TMP=%TEMP%\index.new.%RANDOM%%RANDOM%.html"

if not exist "%TARGET%" (
  echo [ERROR] index.html tidak ditemukan di folder ini.
  pause
  exit /b 1
)

echo URL sumber:
echo %RAW_URL%
echo URL download:
echo %DL_URL%
echo.

copy /Y "%TARGET%" "%BACKUP%" >nul
if errorlevel 1 (
  echo [ERROR] Gagal membuat backup index.html
  pause
  exit /b 1
)

echo Mengunduh versi terbaru index.html...
set "DL_OK=0"

where curl.exe >nul 2>&1
if not errorlevel 1 (
  curl.exe -L --fail --silent --show-error "%DL_URL%" -o "%TMP%"
  if not errorlevel 1 set "DL_OK=1"
)

if "%DL_OK%"=="0" (
  powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "$ErrorActionPreference='Stop';" ^
    "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12;" ^
    "Invoke-WebRequest -Uri '%DL_URL%' -OutFile '%TMP%'"
  if not errorlevel 1 set "DL_OK=1"
)

if "%DL_OK%"=="0" (
  echo [ERROR] Gagal download file dari GitHub.
  echo Restore dari backup...
  copy /Y "%BACKUP%" "%TARGET%" >nul
  if exist "%TMP%" del /f /q "%TMP%" >nul 2>&1
  pause
  exit /b 1
)

for %%A in ("%TMP%") do set "NEW_SIZE=%%~zA"
if "!NEW_SIZE!"=="" set "NEW_SIZE=0"
if !NEW_SIZE! LSS 1000 (
  echo [ERROR] File hasil download terlalu kecil. Kemungkinan URL salah.
  echo Restore dari backup...
  copy /Y "%BACKUP%" "%TARGET%" >nul
  del /f /q "%TMP%" >nul 2>&1
  pause
  exit /b 1
)

copy /Y "%TMP%" "%TARGET%" >nul
if errorlevel 1 (
  echo [ERROR] Gagal mengganti index.html
  echo Restore dari backup...
  copy /Y "%BACKUP%" "%TARGET%" >nul
  if exist "%TMP%" del /f /q "%TMP%" >nul 2>&1
  pause
  exit /b 1
)
if exist "%TMP%" del /f /q "%TMP%" >nul 2>&1

echo [OK] index.html berhasil diperbarui.
echo data.json TIDAK diubah.
echo Backup tersimpan di: index.backup.html
echo.
pause
