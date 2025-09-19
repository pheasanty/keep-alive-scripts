@echo off
title SWallet Keep-Alive
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    SWALLET KEEP-ALIVE                        ║
echo ║                                                              ║
echo ║  Mantiene activa tu API de SWallet en Render                ║
echo ║  URL: https://swallet-troe.onrender.com                     ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado o no está en el PATH
    echo 📥 Descarga Python desde: https://python.org
    pause
    exit /b 1
)

REM Verificar si requests está instalado
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo 📦 Instalando dependencias...
    pip install requests
    if errorlevel 1 (
        echo ❌ Error instalando dependencias
        pause
        exit /b 1
    )
)

echo ✅ Python y dependencias verificadas
echo.

REM Mostrar opciones
echo 🔧 Modos disponibles:
echo    1. Development (5 min interval)
echo    2. Production (25 min interval) - Recomendado
echo    3. Aggressive (15 min interval)
echo.

set /p choice="Selecciona un modo (1-3) o presiona Enter para Production: "

if "%choice%"=="1" (
    set mode=development
    echo 🚀 Iniciando en modo Development...
) else if "%choice%"=="2" (
    set mode=production
    echo 🚀 Iniciando en modo Production...
) else if "%choice%"=="3" (
    set mode=aggressive
    echo 🚀 Iniciando en modo Aggressive...
) else (
    set mode=production
    echo 🚀 Iniciando en modo Production (por defecto)...
)

echo.
echo 📍 URL: https://swallet-troe.onrender.com
echo ⏰ Modo: %mode%
echo 📁 Logs: logs/swallet-keep-alive.log
echo 📊 Estado: logs/swallet-status.json
echo.
echo 💡 Presiona Ctrl+C para detener el script
echo.

python swallet-keep-alive.py %mode%

echo.
echo 🛑 Script detenido
pause
