@echo off
title SWallet Ping - Limpieza de Construccion
color 0C

echo.
echo ================================================================
echo                SWALLET PING - LIMPIEZA                         
echo ================================================================
echo.

echo Limpiando archivos de construccion...
echo.

REM Limpiar archivos de construcción
if exist "build" (
    echo Eliminando carpeta build...
    rmdir /s /q "build"
)

if exist "*.spec" (
    echo Eliminando archivos .spec...
    del "*.spec"
)

if exist "logs" (
    echo Eliminando logs...
    rmdir /s /q "logs"
)

echo.
echo ================================================================
echo                    LIMPIEZA COMPLETADA                         
echo ================================================================
echo.
echo Archivos eliminados:
echo - build/ (archivos de construccion)
echo - *.spec (archivos de configuracion)
echo - logs/ (archivos de log)
echo.
echo El ejecutable dist\SWalletPing.exe se mantiene intacto
echo.
pause
