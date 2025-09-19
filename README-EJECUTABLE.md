# 🚀 SWallet Ping - Ejecutable (.exe)

Ejecutable para mantener activa tu API de SWallet en Render haciendo ping constante cada 20 minutos.

## 📁 Archivos del Ejecutable

### Ejecutable Principal
- **`dist/SWalletPing.exe`** - Ejecutable principal (ya construido)

### Scripts de Construcción
- **`swallet-ping-constant.py`** - Código fuente del ping constante
- **`build-exe.bat`** - Script para construir el ejecutable
- **`swallet-ping.spec`** - Configuración de PyInstaller

### Scripts de Inicio
- **`INICIAR-PING.bat`** - Script principal para iniciar el ejecutable
- **`start-ping-exe.bat`** - Script alternativo de inicio

### Scripts de Prueba
- **`test-ping-constant.py`** - Script de prueba de conectividad

## 🚀 Uso Inmediato

### Opción 1: Script Principal (Recomendado)
```bash
# Doble clic en Windows
INICIAR-PING.bat
```

### Opción 2: Ejecutable Directo
```bash
dist\SWalletPing.exe
```

### Opción 3: Script Alternativo
```bash
start-ping-exe.bat
```

## ⚙️ Características del Ejecutable

### Configuración
- **URL:** https://swallet-troe.onrender.com
- **Intervalo:** 20 minutos (Render se cierra después de 30 min)
- **Endpoints:** `/api`, `/api/health`, `/api/info`
- **Timeout:** 30 segundos por request

### Funcionalidades
- ✅ **Ping automático** cada 20 minutos
- ✅ **Múltiples endpoints** monitoreados
- ✅ **Logging completo** en archivos
- ✅ **Manejo de errores** robusto
- ✅ **Cierre graceful** con Ctrl+C
- ✅ **Estado persistente** en JSON
- ✅ **Reintentos automáticos** en caso de fallos

### Logs
- **Archivo:** `logs/swallet-ping.log`
- **Estado:** `logs/swallet-ping-status.json`

## 🔧 Construcción del Ejecutable

### Requisitos
- Python 3.6+
- PyInstaller
- Biblioteca `requests`

### Construcción Automática
```bash
# Ejecutar script de construcción
build-exe.bat
```

### Construcción Manual
```bash
# Instalar dependencias
pip install requests pyinstaller

# Construir ejecutable
python -m PyInstaller --onefile --console --name "SWalletPing" swallet-ping-constant.py
```

## 📊 Monitoreo

### Ver Estado Actual
El ejecutable muestra en tiempo real:
- Número de ping actual
- Hora del último ping
- Estado de cada endpoint
- Resultado del ping
- Tiempo hasta el próximo ping

### Logs Detallados
Revisa `logs/swallet-ping.log` para:
- Historial completo de pings
- Errores de conectividad
- Tiempos de respuesta
- Fallos consecutivos

### Estado JSON
Revisa `logs/swallet-ping-status.json` para:
- Último ping realizado
- Contador total de pings
- Fallos consecutivos
- Estado de la API
- Configuración actual

## 🚨 Solución de Problemas

### Error: "El ejecutable no existe"
```bash
# Construir el ejecutable
build-exe.bat
```

### Error: "No se puede conectar a la API"
1. Verifica tu conexión a internet
2. Confirma que la API esté funcionando: https://swallet-troe.onrender.com/api
3. Revisa los logs para errores específicos

### El ejecutable se cierra inesperadamente
1. Revisa los logs en `logs/swallet-ping.log`
2. Verifica que no haya problemas de conectividad
3. Ejecuta `test-ping-constant.py` para probar la conectividad

### La API se sigue cerrando
1. Verifica que el ejecutable esté funcionando
2. Confirma que esté haciendo ping cada 20 minutos
3. Revisa los logs para confirmar que los pings son exitosos

## 📱 Ejecutar como Servicio

### Windows (Task Scheduler)
1. Abre "Programador de tareas"
2. Crea una tarea básica
3. Configura para ejecutar `dist\SWalletPing.exe`
4. Establece para ejecutar al inicio del sistema
5. Configura para ejecutar en segundo plano

### Windows (Servicio)
1. Usa herramientas como NSSM (Non-Sucking Service Manager)
2. Instala el ejecutable como servicio de Windows
3. Configura para iniciar automáticamente

## 🎯 Recomendaciones

1. **Ejecuta el programa 24/7** para mantener la API activa
2. **Monitorea los logs** regularmente
3. **Configura alertas** si la API falla repetidamente
4. **Mantén el programa ejecutándose** en un servidor o computadora que esté siempre encendida
5. **Verifica periódicamente** que el programa esté funcionando

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs en `logs/swallet-ping.log`
2. Ejecuta `test-ping-constant.py` para probar conectividad
3. Verifica la configuración en `logs/swallet-ping-status.json`
4. Confirma que la API esté funcionando manualmente

## 🎉 ¡Listo!

Tu ejecutable está listo para mantener activa tu API de SWallet. Solo ejecuta `INICIAR-PING.bat` y tu API nunca más se cerrará por inactividad.

**¡Disfruta de tu API siempre activa!** 🚀
