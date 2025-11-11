@echo off
title Keep Alive Advanced - Ejecutable
color 0A

echo.
echo ================================================================
echo          KEEP ALIVE ADVANCED - MANTENIENDO APIs ACTIVAS          
echo ================================================================
echo.

REM Verificar si el ejecutable existe
if not exist "dist\KeepAliveAdvanced.exe" (
    echo ERROR: El ejecutable no existe
    echo.
    echo Por favor ejecuta primero: build-keep-alive-advanced.bat
    echo.
    pause
    exit /b 1
)

echo Iniciando Keep Alive Advanced...
echo.
echo APIs que se mantendran activas:
echo   - SWallet: https://swallet-troe.onrender.com
echo   - Emilia Bot: https://backendbotemilia.onrender.com
echo.
echo Intervalo: 30 segundos
echo.
echo Presiona Ctrl+C para detener
echo.

REM Ejecutar el ejecutable con el modo especificado (si se proporciona)
if "%1"=="" (
    dist\KeepAliveAdvanced.exe production
) else (
    dist\KeepAliveAdvanced.exe %1
)

