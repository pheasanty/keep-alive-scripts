@echo off
title SWallet Ping - Prueba del Ejecutable
color 0B

echo.
echo ================================================================
echo                SWALLET PING - PRUEBA DEL EXE                   
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

echo Probando conectividad con la API...
echo URL: https://swallet-troe.onrender.com
echo.

python test-ping-constant.py

echo.
echo ================================================================
echo.
echo Si la prueba fue exitosa, puedes ejecutar el ejecutable:
echo.
echo 1. INICIAR-PING.bat (Recomendado)
echo 2. dist\SWalletPing.exe (Directo)
echo.
echo El ejecutable hara ping cada 20 minutos automaticamente
echo.
pause
