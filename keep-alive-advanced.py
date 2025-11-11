#!/usr/bin/env python3
"""
Script avanzado de keep-alive con configuración flexible
"""

import requests
import time
import logging
import json
import sys
import os
from datetime import datetime
from pathlib import Path
from config import get_config

# Configurar encoding UTF-8 para stdout en Windows
if sys.platform == 'win32':
    try:
        # Intentar configurar stdout para UTF-8
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        elif hasattr(sys.stdout, 'buffer'):
            # Para versiones más antiguas de Python
            import io
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass  # Si falla, continuar con el encoding por defecto

class SafeStreamHandler(logging.StreamHandler):
    """StreamHandler que maneja errores de encoding UTF-8 en Windows"""
    def emit(self, record):
        try:
            msg = self.format(record)
            stream = self.stream
            # Intentar escribir con UTF-8, si falla usar replace para caracteres inválidos
            try:
                stream.write(msg + self.terminator)
            except UnicodeEncodeError:
                # Reemplazar caracteres que no se pueden codificar
                stream.write(msg.encode('ascii', 'replace').decode('ascii') + self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)

def setup_logging(config):
    """Configura el sistema de logging"""
    log_dir = Path(config.LOG_DIR)
    log_dir.mkdir(exist_ok=True)
    
    # Configurar nivel de logging
    log_level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)
    
    # Configurar handlers
    handlers = [
        logging.FileHandler(log_dir / 'keep-alive.log', encoding='utf-8'),
        SafeStreamHandler(sys.stdout)
    ]
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=handlers,
        force=True
    )
    
    return logging.getLogger(__name__)

def ping_url(url, api_name, logger, timeout):
    """Hace un ping a una URL específica"""
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            logger.info(f"✅ [{api_name}] {url} - Status: {response.status_code}")
            return True
        else:
            logger.warning(f"⚠️ [{api_name}] {url} - Status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ [{api_name}] {url} - Error: {e}")
        return False

def ping_endpoint(endpoint, config, logger):
    """Hace un ping a un endpoint específico (compatibilidad)"""
    url = f"{config.API_BASE_URL}{endpoint}"
    return ping_url(url, "SWallet", logger, config.TIMEOUT)

def ping_all_endpoints(config, logger):
    """Hace ping a todos los endpoints de todas las APIs configuradas"""
    logger.info("🔄 Iniciando ping a todas las APIs...")
    total_successful = 0
    total_endpoints = 0
    api_results = {}
    
    # Hacer ping a todas las APIs configuradas
    for api_config in config.get_apis():
        api_name = api_config.name
        api_successful = 0
        api_total = len(api_config.endpoints)
        total_endpoints += api_total
        
        logger.info(f"📡 Ping a API: {api_name} ({api_config.base_url})")
        
        for endpoint in api_config.endpoints:
            url = f"{api_config.base_url}{endpoint}"
            if ping_url(url, api_name, logger, config.TIMEOUT):
                api_successful += 1
                total_successful += 1
            time.sleep(1)  # Pequeña pausa entre pings
        
        api_results[api_name] = {
            'successful': api_successful,
            'total': api_total,
            'status': 'healthy' if api_successful == api_total else 'degraded' if api_successful > 0 else 'down'
        }
        
        logger.info(f"📊 [{api_name}] Resultado: {api_successful}/{api_total} endpoints respondieron correctamente")
        time.sleep(2)  # Pausa entre APIs
    
    logger.info(f"📊 Resultado General: {total_successful}/{total_endpoints} endpoints respondieron correctamente")
    return total_successful > 0, api_results

def save_status(status_data, config):
    """Guarda el estado actual en un archivo JSON"""
    status_file = Path(config.LOG_DIR) / "api-status.json"
    try:
        with open(status_file, 'w') as f:
            json.dump(status_data, f, indent=2)
    except Exception as e:
        print(f"❌ Error guardando estado: {e}")

def main():
    """Función principal del script"""
    # Obtener modo desde argumentos o variable de entorno
    mode = sys.argv[1] if len(sys.argv) > 1 else os.getenv('MODE', 'production')
    
    # Obtener configuración
    config = get_config(mode)
    
    # Configurar logging
    logger = setup_logging(config)
    
    logger.info("🚀 Iniciando script avanzado de keep-alive para múltiples APIs")
    logger.info(f"⏰ Intervalo: {config.get_ping_interval()} segundos ({config.get_ping_interval()/60:.1f} minutos)")
    logger.info(f"🔧 Modo: {config.MODE}")
    logger.info(f"📊 Nivel de Log: {config.LOG_LEVEL}")
    logger.info(f"🌐 APIs configuradas: {len(config.get_apis())}")
    for api_config in config.get_apis():
        logger.info(f"  - {api_config.name}: {api_config.base_url} ({len(api_config.endpoints)} endpoints)")
    
    ping_count = 0
    consecutive_failures = 0
    
    while True:
        try:
            ping_count += 1
            current_time = datetime.now()
            
            logger.info(f"🔄 Ping #{ping_count} - {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Hacer ping a todos los endpoints de todas las APIs
            success, api_results = ping_all_endpoints(config, logger)
            
            if success:
                consecutive_failures = 0
                logger.info("✅ Todas las APIs funcionando correctamente")
            else:
                consecutive_failures += 1
                logger.warning(f"⚠️ Algunas APIs con problemas - Fallos consecutivos: {consecutive_failures}")
            
            # Guardar estado
            status_data = {
                "last_ping": current_time.isoformat(),
                "ping_count": ping_count,
                "consecutive_failures": consecutive_failures,
                "overall_status": "healthy" if consecutive_failures == 0 else "degraded",
                "apis": api_results,
                "mode": config.MODE,
                "config": {
                    "ping_interval": config.get_ping_interval(),
                    "timeout": config.get_timeout(),
                    "log_level": config.get_log_level()
                }
            }
            save_status(status_data, config)
            
            # Si hay muchos fallos consecutivos, esperar menos tiempo
            if consecutive_failures >= 3:
                wait_time = 5 * 60  # 5 minutos
                logger.warning(f"🚨 Muchos fallos consecutivos, esperando solo {wait_time/60:.1f} minutos...")
            else:
                wait_time = config.get_ping_interval()
            
            logger.info(f"😴 Esperando {wait_time} segundos hasta el próximo ping...")
            time.sleep(wait_time)
            
        except KeyboardInterrupt:
            logger.info("🛑 Script interrumpido por el usuario")
            break
        except Exception as e:
            logger.error(f"❌ Error inesperado: {e}")
            logger.info("🔄 Continuando en 5 minutos...")
            time.sleep(300)

if __name__ == "__main__":
    main()
