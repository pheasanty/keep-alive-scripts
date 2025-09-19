# 🚀 Script Keep-Alive para SWallet API

Este script mantiene activa tu API de SWallet en Render haciendo pings periódicos para evitar que se cierre por inactividad.

## 📋 Requisitos

- Python 3.6+
- Biblioteca `requests`

## 🛠️ Instalación

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Hacer ejecutable el script (Linux/Mac):**
   ```bash
   chmod +x start-keep-alive.sh
   ```

## 🚀 Uso

### Opción 1: Script Simple
```bash
python keep-alive.py
```

### Opción 2: Script Avanzado (Recomendado)
```bash
python keep-alive-service.py
```

### Opción 3: Scripts de Inicio
- **Windows:** Doble clic en `start-keep-alive.bat`
- **Linux/Mac:** `./start-keep-alive.sh`

## ⚙️ Configuración

### Script Simple (`keep-alive.py`)
- **Intervalo:** 25 minutos
- **Endpoint:** `/api`
- **Timeout:** 30 segundos

### Script Avanzado (`keep-alive-service.py`)
- **Intervalo:** 25 minutos
- **Endpoints:** `/api`, `/api/health`, `/api/info`, `/api/users/stats`
- **Timeout:** 30 segundos
- **Logs:** Guardados en `logs/keep-alive.log`
- **Estado:** Guardado en `logs/api-status.json`

## 📊 Monitoreo

### Logs
Los logs se guardan en:
- `keep-alive.log` (script simple)
- `logs/keep-alive.log` (script avanzado)

### Estado de la API
El script avanzado guarda el estado en `logs/api-status.json`:
```json
{
  "last_ping": "2025-01-19T12:30:00",
  "ping_count": 150,
  "consecutive_failures": 0,
  "api_status": "healthy",
  "endpoints": ["/api", "/api/health", "/api/info", "/api/users/stats"]
}
```

## 🔧 Personalización

### Cambiar el intervalo de ping
Edita la variable `PING_INTERVAL` en el script:
```python
PING_INTERVAL = 20 * 60  # 20 minutos
```

### Agregar más endpoints
En el script avanzado, modifica la lista `ENDPOINTS`:
```python
ENDPOINTS = [
    "/api",
    "/api/health", 
    "/api/info",
    "/api/users/stats",
    "/api/users"  # Nuevo endpoint
]
```

## 🚨 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'requests'"
```bash
pip install requests
```

### Error: "Permission denied" (Linux/Mac)
```bash
chmod +x start-keep-alive.sh
```

### La API no responde
1. Verifica que la URL sea correcta
2. Revisa los logs para ver errores específicos
3. Asegúrate de que la API esté desplegada correctamente

## 📱 Ejecutar como Servicio

### Windows (Task Scheduler)
1. Abre "Programador de tareas"
2. Crea una tarea básica
3. Configura para ejecutar `python keep-alive-service.py`
4. Establece para ejecutar al inicio del sistema

### Linux (systemd)
1. Crea el archivo `/etc/systemd/system/swallet-keepalive.service`:
```ini
[Unit]
Description=SWallet API Keep-Alive Service
After=network.target

[Service]
Type=simple
User=tu_usuario
WorkingDirectory=/ruta/a/tu/proyecto
ExecStart=/usr/bin/python3 keep-alive-service.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

2. Habilita el servicio:
```bash
sudo systemctl enable swallet-keepalive.service
sudo systemctl start swallet-keepalive.service
```

## 🎯 Recomendaciones

1. **Usa el script avanzado** para mejor monitoreo
2. **Ejecuta en un servidor** para mantener la API activa 24/7
3. **Monitorea los logs** regularmente
4. **Configura alertas** si la API falla repetidamente

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs
2. Verifica la conectividad a internet
3. Confirma que la API esté funcionando manualmente
4. Revisa la configuración de Render

¡Tu API de SWallet se mantendrá activa! 🎉
