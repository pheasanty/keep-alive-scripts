@echo off
title Keep Alive Advanced - Construccion de Ejecutable
color 0B

echo.
echo ================================================================
echo          KEEP ALIVE ADVANCED - CONSTRUCCION EXE                 
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
pip install requests pyinstaller >nul 2>&1
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias
    echo Intenta ejecutar: pip install requests pyinstaller
    pause
    exit /b 1
)

echo.
echo OK: Dependencias instaladas correctamente
echo.

REM Limpiar archivos anteriores del ejecutable específico
echo Limpiando archivos anteriores de KeepAliveAdvanced...
if exist "dist\KeepAliveAdvanced.exe" del "dist\KeepAliveAdvanced.exe"
if exist "build\KeepAliveAdvanced" rmdir /s /q "build\KeepAliveAdvanced"

echo.
echo Construyendo ejecutable...
python -m PyInstaller --onefile --console --name "KeepAliveAdvanced" keep-alive-advanced.py

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
echo El ejecutable se ha creado en: dist\KeepAliveAdvanced.exe
echo.
echo Para ejecutar:
echo   dist\KeepAliveAdvanced.exe
echo.
echo O con modo especifico:
echo   dist\KeepAliveAdvanced.exe production
echo   dist\KeepAliveAdvanced.exe development
echo   dist\KeepAliveAdvanced.exe aggressive
echo.
echo El ejecutable mantendra activas las siguientes APIs:
echo   - SWallet: https://swallet-troe.onrender.com
echo   - Emilia Bot: https://backendbotemilia.onrender.com
echo.
echo Intervalo de ping: 30 segundos (modo production)
echo.
pause

