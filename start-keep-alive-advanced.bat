@echo off
echo 🚀 Iniciando script avanzado de keep-alive para SWallet API...
echo.

REM Cargar variables de entorno si existe el archivo
if exist keep-alive.env (
    echo 📋 Cargando configuración desde keep-alive.env...
    for /f "usebackq tokens=1,2 delims==" %%a in ("keep-alive.env") do (
        if not "%%a"=="" if not "%%a:~0,1%"=="#" (
            set %%a=%%b
        )
    )
)

echo 📍 URL: %API_BASE_URL%
echo ⏰ Intervalo: %PING_INTERVAL% segundos
echo 🔧 Modo: %MODE%
echo 📊 Nivel de Log: %LOG_LEVEL%
echo.

echo Presiona Ctrl+C para detener el script
echo.

python keep-alive-advanced.py %MODE%

pause
