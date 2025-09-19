@echo off
title SWallet Ping - Mantener API Activa
color 0A

echo.
echo ================================================================
echo                    SWALLET PING CONSTANTE                      
echo ================================================================
echo.
echo Este programa mantiene activa tu API de SWallet en Render
echo URL: https://swallet-troe.onrender.com
echo Intervalo: 20 minutos
echo.
echo IMPORTANTE: 
echo - Manten este programa ejecutandose para que tu API no se cierre
echo - Presiona Ctrl+C para detener el programa
echo - Los logs se guardan en la carpeta 'logs'
echo.
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
echo.

dist\SWalletPing.exe

echo.
echo ================================================================
echo                    SWALLET PING DETENIDO                      
echo ================================================================
echo.
echo El programa se ha detenido.
echo Tu API puede cerrarse por inactividad.
echo.
pause
