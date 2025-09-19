# 🚀 SWallet Keep-Alive System

Sistema completo para mantener activa tu API de SWallet en Render, evitando que se cierre por inactividad.

## 📋 Archivos Incluidos

### Scripts Principales
- **`swallet-keep-alive.py`** - Script principal con todas las funcionalidades
- **`start-swallet-keep-alive.bat`** - Script de inicio para Windows con interfaz
- **`keep-alive.py`** - Script simple básico
- **`keep-alive-advanced.py`** - Script avanzado con configuración
- **`test-ping.py`** - Script de prueba rápida

### Configuración
- **`config.py`** - Configuración flexible para diferentes modos
- **`keep-alive.env`** - Variables de entorno de ejemplo
- **`requirements.txt`** - Dependencias de Python

### Utilidades
- **`monitor-status.py`** - Monitor del estado de la API
- **`start-keep-alive.bat`** - Script de inicio simple
- **`start-keep-alive.sh`** - Script de inicio para Linux/Mac

## 🚀 Uso Rápido

### Opción 1: Script Principal (Recomendado)
```bash
# Doble clic en Windows
start-swallet-keep-alive.bat

# O desde terminal
python swallet-keep-alive.py production
```

### Opción 2: Script Simple
```bash
python keep-alive.py
```

### Opción 3: Script Avanzado
```bash
python keep-alive-advanced.py production
```

## 🔧 Modos de Operación

### Development
- **Intervalo:** 5 minutos
- **Endpoints:** `/api`, `/api/health`
- **Timeout:** 10 segundos
- **Logging:** DEBUG

### Production (Recomendado)
- **Intervalo:** 25 minutos
- **Endpoints:** `/api`, `/api/health`, `/api/info`, `/api/users/stats`
- **Timeout:** 30 segundos
- **Logging:** INFO

### Aggressive
- **Intervalo:** 15 minutos
- **Endpoints:** `/api`, `/api/health`, `/api/info`, `/api/users/stats`
- **Timeout:** 20 segundos
- **Logging:** INFO

## 📊 Monitoreo

### Ver Estado Actual
```bash
python monitor-status.py
```

### Logs
- **Principal:** `logs/swallet-keep-alive.log`
- **Estado:** `logs/swallet-status.json`

### Prueba Rápida
```bash
python test-ping.py
```

## 🛠️ Instalación

### Requisitos
- Python 3.6+
- Biblioteca `requests`

### Instalación Automática
El script `start-swallet-keep-alive.bat` instala automáticamente las dependencias.

### Instalación Manual
```bash
pip install -r requirements.txt
```

## ⚙️ Configuración Avanzada

### Variables de Entorno
Crea un archivo `.env` basado en `keep-alive.env`:
```env
API_BASE_URL=https://swallet-troe.onrender.com
PING_INTERVAL=1500
TIMEOUT=30
MODE=production
```

### Personalización
Edita `config.py` para modificar:
- Intervalos de ping
- Endpoints a monitorear
- Timeouts
- Niveles de logging

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
2. Revisa los logs en `logs/swallet-keep-alive.log`
3. Ejecuta `python test-ping.py` para probar conectividad

### Script se detiene inesperadamente
1. Revisa los logs para errores
2. Verifica la conectividad a internet
3. Confirma que la API esté funcionando

## 📱 Ejecutar como Servicio

### Windows (Task Scheduler)
1. Abre "Programador de tareas"
2. Crea una tarea básica
3. Configura para ejecutar `python swallet-keep-alive.py production`
4. Establece para ejecutar al inicio del sistema

### Linux (systemd)
1. Crea `/etc/systemd/system/swallet-keepalive.service`:
```ini
[Unit]
Description=SWallet API Keep-Alive Service
After=network.target

[Service]
Type=simple
User=tu_usuario
WorkingDirectory=/ruta/a/tu/proyecto
ExecStart=/usr/bin/python3 swallet-keep-alive.py production
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

1. **Usa el script principal** (`swallet-keep-alive.py`) para mejor funcionalidad
2. **Ejecuta en modo Production** para uso normal
3. **Ejecuta en un servidor** para mantener la API activa 24/7
4. **Monitorea los logs** regularmente
5. **Configura alertas** si la API falla repetidamente

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs en `logs/swallet-keep-alive.log`
2. Ejecuta `python monitor-status.py` para ver el estado
3. Prueba la conectividad con `python test-ping.py`
4. Verifica la configuración en `logs/swallet-status.json`

## 🎉 ¡Listo!

Tu API de SWallet se mantendrá activa y no se cerrará por inactividad. El sistema está diseñado para ser robusto y manejar errores automáticamente.

**¡Disfruta de tu API siempre activa!** 🚀
