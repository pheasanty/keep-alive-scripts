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

def setup_logging(config):
    """Configura el sistema de logging"""
    log_dir = Path(config.LOG_DIR)
    log_dir.mkdir(exist_ok=True)
    
    # Configurar nivel de logging
    log_level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / 'keep-alive.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__)

def ping_endpoint(endpoint, config, logger):
    """Hace un ping a un endpoint específico"""
    url = f"{config.API_BASE_URL}{endpoint}"
    try:
        response = requests.get(url, timeout=config.TIMEOUT)
        if response.status_code == 200:
            logger.info(f"✅ {endpoint} - Status: {response.status_code}")
            return True
        else:
            logger.warning(f"⚠️ {endpoint} - Status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ {endpoint} - Error: {e}")
        return False

def ping_all_endpoints(config, logger):
    """Hace ping a todos los endpoints configurados"""
    logger.info("🔄 Iniciando ping a todos los endpoints...")
    successful_pings = 0
    
    for endpoint in config.get_endpoints():
        if ping_endpoint(endpoint, config, logger):
            successful_pings += 1
        time.sleep(2)  # Pequeña pausa entre pings
    
    logger.info(f"📊 Resultado: {successful_pings}/{len(config.get_endpoints())} endpoints respondieron correctamente")
    return successful_pings > 0

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
    
    logger.info("🚀 Iniciando script avanzado de keep-alive para SWallet API")
    logger.info(f"📍 URL Base: {config.API_BASE_URL}")
    logger.info(f"🎯 Endpoints: {', '.join(config.get_endpoints())}")
    logger.info(f"⏰ Intervalo: {config.get_ping_interval()} segundos ({config.get_ping_interval()/60:.1f} minutos)")
    logger.info(f"🔧 Modo: {config.MODE}")
    logger.info(f"📊 Nivel de Log: {config.LOG_LEVEL}")
    
    ping_count = 0
    consecutive_failures = 0
    
    while True:
        try:
            ping_count += 1
            current_time = datetime.now()
            
            logger.info(f"🔄 Ping #{ping_count} - {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Hacer ping a todos los endpoints
            if ping_all_endpoints(config, logger):
                consecutive_failures = 0
                logger.info("✅ API funcionando correctamente")
            else:
                consecutive_failures += 1
                logger.warning(f"⚠️ API con problemas - Fallos consecutivos: {consecutive_failures}")
            
            # Guardar estado
            status_data = {
                "last_ping": current_time.isoformat(),
                "ping_count": ping_count,
                "consecutive_failures": consecutive_failures,
                "api_status": "healthy" if consecutive_failures == 0 else "degraded",
                "endpoints": config.get_endpoints(),
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
