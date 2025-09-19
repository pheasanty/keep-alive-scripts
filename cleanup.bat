@echo off
echo Limpiando archivos temporales...

REM Eliminar archivos de log si existen
if exist "..\logs\keep-alive.log" del "..\logs\keep-alive.log"
if exist "..\logs\swallet-keep-alive.log" del "..\logs\swallet-keep-alive.log"
if exist "..\logs\api-status.json" del "..\logs\api-status.json"
if exist "..\logs\swallet-status.json" del "..\logs\swallet-status.json"

REM Eliminar archivos de log en la carpeta actual
if exist "logs\keep-alive.log" del "logs\keep-alive.log"
if exist "logs\swallet-keep-alive.log" del "logs\swallet-keep-alive.log"
if exist "logs\api-status.json" del "logs\api-status.json"
if exist "logs\swallet-status.json" del "logs\swallet-status.json"

echo Limpieza completada.
pause
