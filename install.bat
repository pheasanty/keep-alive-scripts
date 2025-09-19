@echo off
title SWallet Keep-Alive - Instalacion
color 0B

echo.
echo ================================================================
echo                SWALLET KEEP-ALIVE - INSTALACION               
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
pip install requests
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias
    echo Intenta ejecutar: pip install requests
    pause
    exit /b 1
)

echo.
echo OK: Dependencias instaladas correctamente
echo.
echo ================================================================
echo                    INSTALACION COMPLETADA                      
echo ================================================================
echo.
echo Para usar el sistema:
echo   1. Ejecuta: start-swallet-keep-alive-fixed.bat
echo   2. O desde terminal: python swallet-keep-alive-fixed.py production
echo.
echo Para probar la conectividad:
echo   python test-ping-fixed.py
echo.
echo Para limpiar archivos temporales:
echo   cleanup.bat
echo.
pause
