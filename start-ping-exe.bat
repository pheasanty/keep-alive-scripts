@echo off
title SWallet Ping - Ejecutable
color 0A

echo.
echo ================================================================
echo                    SWALLET PING EJECUTABLE                      
echo ================================================================
echo.

REM Verificar si el ejecutable existe
if not exist "dist\SWalletPing.exe" (
    echo ERROR: El ejecutable no existe
    echo.
    echo Ejecuta primero: build-exe.bat
    echo.
    pause
    exit /b 1
)

echo Iniciando SWallet Ping...
echo URL: https://swallet-troe.onrender.com
echo Intervalo: 20 minutos
echo.
echo Presiona Ctrl+C para detener
echo.

dist\SWalletPing.exe

echo.
echo SWallet Ping detenido
pause
