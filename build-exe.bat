@echo off
title SWallet Ping - Construccion de Ejecutable
color 0B

echo.
echo ================================================================
echo                SWALLET PING - CONSTRUCCION EXE                 
echo ================================================================
echo.

REM Verificar si Python está instalado
echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo.
    echo Por favor instala Python desde: https://python.org
    echo Asegurate de marcar "Add Python to PATH" durante la instalacion
    echo.
    pause
    exit /b 1
)

echo OK: Python encontrado
python --version

echo.
echo Instalando dependencias...
pip install requests pyinstaller
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias
    echo Intenta ejecutar: pip install requests pyinstaller
    pause
    exit /b 1
)

echo.
echo OK: Dependencias instaladas correctamente
echo.

REM Limpiar archivos anteriores
echo Limpiando archivos anteriores...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "*.spec" del "*.spec"

echo.
echo Construyendo ejecutable...
pyinstaller --onefile --console --name "SWalletPing" swallet-ping-constant.py

if errorlevel 1 (
    echo ERROR: Error construyendo el ejecutable
    pause
    exit /b 1
)

echo.
echo ================================================================
echo                    CONSTRUCCION COMPLETADA                     
echo ================================================================
echo.
echo El ejecutable se ha creado en: dist\SWalletPing.exe
echo.
echo Para ejecutar:
echo   dist\SWalletPing.exe
echo.
echo El ejecutable hara ping cada 30 segundos para mantener tu API activa
echo.
pause
