#!/usr/bin/env python3
"""
Script avanzado para mantener activa la API de SWallet en Render
Incluye múltiples endpoints y manejo de errores mejorado
"""

import requests
import time
import logging
import json
from datetime import datetime
import sys
import os
from pathlib import Path

# Configuración
API_BASE_URL = "https://swallet-troe.onrender.com"
ENDPOINTS = [
    "/api",
    "/api/health", 
    "/api/info",
    "/api/users/stats"
]
PING_INTERVAL = 25 * 60  # 25 minutos
TIMEOUT = 30
MAX_RETRIES = 3

# Configurar logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / 'keep-alive.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def ping_endpoint(endpoint):
    """Hace un ping a un endpoint específico"""
    url = f"{API_BASE_URL}{endpoint}"
    try:
        response = requests.get(url, timeout=TIMEOUT)
        if response.status_code == 200:
            logger.info(f"✅ {endpoint} - Status: {response.status_code}")
            return True
        else:
            logger.warning(f"⚠️ {endpoint} - Status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ {endpoint} - Error: {e}")
        return False

def ping_all_endpoints():
    """Hace ping a todos los endpoints configurados"""
    logger.info("🔄 Iniciando ping a todos los endpoints...")
    successful_pings = 0
    
    for endpoint in ENDPOINTS:
        if ping_endpoint(endpoint):
            successful_pings += 1
        time.sleep(2)  # Pequeña pausa entre pings
    
    logger.info(f"📊 Resultado: {successful_pings}/{len(ENDPOINTS)} endpoints respondieron correctamente")
    return successful_pings > 0

def save_status(status_data):
    """Guarda el estado actual en un archivo JSON"""
    status_file = log_dir / "api-status.json"
    try:
        with open(status_file, 'w') as f:
            json.dump(status_data, f, indent=2)
    except Exception as e:
        logger.error(f"❌ Error guardando estado: {e}")

def main():
    """Función principal del script"""
    logger.info("🚀 Iniciando script avanzado de keep-alive para SWallet API")
    logger.info(f"📍 URL Base: {API_BASE_URL}")
    logger.info(f"🎯 Endpoints: {', '.join(ENDPOINTS)}")
    logger.info(f"⏰ Intervalo: {PING_INTERVAL} segundos ({PING_INTERVAL/60:.1f} minutos)")
    
    ping_count = 0
    consecutive_failures = 0
    
    while True:
        try:
            ping_count += 1
            current_time = datetime.now()
            
            logger.info(f"🔄 Ping #{ping_count} - {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Hacer ping a todos los endpoints
            if ping_all_endpoints():
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
                "endpoints": ENDPOINTS
            }
            save_status(status_data)
            
            # Si hay muchos fallos consecutivos, esperar menos tiempo
            if consecutive_failures >= 3:
                wait_time = 5 * 60  # 5 minutos
                logger.warning(f"🚨 Muchos fallos consecutivos, esperando solo {wait_time/60:.1f} minutos...")
            else:
                wait_time = PING_INTERVAL
            
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
