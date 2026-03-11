@echo off
setlocal EnableExtensions EnableDelayedExpansion

echo =====================================
echo   Manajemen Asset BNNK Sleman
echo   Update semua file dari GitHub
echo =====================================
echo.

REM Optional argument:
REM UPDATE_INDEX.bat https://github.com/USERNAME/REPO/archive/refs/heads/main.zip
set "ZIP_URL=%~1"
if "%ZIP_URL%"=="" set "ZIP_URL=https://github.com/vsh2607/simple-asset-management/archive/refs/heads/main.zip"

set "BASE_DIR=%~dp0"
set "TMP_ZIP=%TEMP%\asset_update_%RANDOM%%RANDOM%.zip"
set "TMP_DIR=%TEMP%\asset_update_%RANDOM%%RANDOM%"
set "SRC_DIR="

echo URL sumber:
echo %ZIP_URL%
echo Folder target:
echo %BASE_DIR%
echo.
echo Catatan:
echo - Semua file akan diperbarui dari GitHub
echo - data.json TIDAK akan diubah
echo.

echo Mengunduh paket update...
set "DL_OK=0"

where curl.exe >nul 2>&1
if not errorlevel 1 (
  curl.exe -L --fail --silent --show-error "%ZIP_URL%" -o "%TMP_ZIP%"
  if not errorlevel 1 set "DL_OK=1"
)

if "%DL_OK%"=="0" (
  powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "$ErrorActionPreference='Stop';" ^
    "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12;" ^
    "Invoke-WebRequest -Uri '%ZIP_URL%' -OutFile '%TMP_ZIP%'"
  if not errorlevel 1 set "DL_OK=1"
)

if "%DL_OK%"=="0" (
  echo [ERROR] Gagal download paket update dari GitHub.
  if exist "%TMP_ZIP%" del /f /q "%TMP_ZIP%" >nul 2>&1
  pause
  exit /b 1
)

for %%A in ("%TMP_ZIP%") do set "NEW_SIZE=%%~zA"
if "!NEW_SIZE!"=="" set "NEW_SIZE=0"
if !NEW_SIZE! LSS 1000 (
  echo [ERROR] File ZIP terlalu kecil. Kemungkinan URL salah.
  del /f /q "%TMP_ZIP%" >nul 2>&1
  pause
  exit /b 1
)

if not exist "%TMP_DIR%" mkdir "%TMP_DIR%" >nul 2>&1

echo Mengekstrak ZIP...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$ErrorActionPreference='Stop';" ^
  "Expand-Archive -Path '%TMP_ZIP%' -DestinationPath '%TMP_DIR%' -Force"
if errorlevel 1 (
  echo [ERROR] Gagal ekstrak ZIP.
  if exist "%TMP_ZIP%" del /f /q "%TMP_ZIP%" >nul 2>&1
  if exist "%TMP_DIR%" rmdir /s /q "%TMP_DIR%" >nul 2>&1
  pause
  exit /b 1
)

for /d %%D in ("%TMP_DIR%\*") do (
  set "SRC_DIR=%%~fD"
  goto :found_src
)

:found_src
if "%SRC_DIR%"=="" (
  echo [ERROR] Folder sumber tidak ditemukan di paket ZIP.
  if exist "%TMP_ZIP%" del /f /q "%TMP_ZIP%" >nul 2>&1
  if exist "%TMP_DIR%" rmdir /s /q "%TMP_DIR%" >nul 2>&1
  pause
  exit /b 1
)

echo Menyalin file update (kecuali data.json)...
robocopy "%SRC_DIR%" "%BASE_DIR%" /E /XF data.json /R:1 /W:1
set "RC=%ERRORLEVEL%"

if %RC% GEQ 8 (
  echo [WARN] Robocopy gagal. Kode: %RC%
  echo Mencoba metode cadangan (PowerShell Copy-Item)...
  powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "$ErrorActionPreference='Stop';" ^
    "$src = [IO.Path]::GetFullPath('%SRC_DIR%');" ^
    "$dst = [IO.Path]::GetFullPath('%BASE_DIR%');" ^
    "Get-ChildItem -LiteralPath $src -Recurse -Force | ForEach-Object {" ^
    "  $rel = $_.FullName.Substring($src.Length).TrimStart('\');" ^
    "  if ($rel -ieq 'data.json') { return }" ^
    "  $target = Join-Path $dst $rel;" ^
    "  if ($_.PSIsContainer) { New-Item -ItemType Directory -Force -Path $target | Out-Null }" ^
    "  else { New-Item -ItemType Directory -Force -Path (Split-Path $target) | Out-Null; Copy-Item -LiteralPath $_.FullName -Destination $target -Force }" ^
    "}"
  if errorlevel 1 (
    echo [ERROR] Fallback copy juga gagal.
    if exist "%TMP_ZIP%" del /f /q "%TMP_ZIP%" >nul 2>&1
    if exist "%TMP_DIR%" rmdir /s /q "%TMP_DIR%" >nul 2>&1
    pause
    exit /b 1
  )
)

if exist "%TMP_ZIP%" del /f /q "%TMP_ZIP%" >nul 2>&1
if exist "%TMP_DIR%" rmdir /s /q "%TMP_DIR%" >nul 2>&1

echo [OK] Update selesai.
echo data.json TIDAK diubah.
echo Semua file lain sudah disinkronkan.
echo.
pause
