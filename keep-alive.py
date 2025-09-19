#!/usr/bin/env python3
"""
Script para mantener activa la API de SWallet en Render
Hace pings periódicos para evitar que se cierre por inactividad
"""

import requests
import time
import logging
from datetime import datetime
import sys

# Configuración
API_URL = "https://swallet-troe.onrender.com/api"
PING_INTERVAL = 25 * 60  # 25 minutos (Render se cierra después de 30 min de inactividad)
TIMEOUT = 30  # Timeout para las requests

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('keep-alive.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def ping_api():
    """Hace un ping a la API para mantenerla activa"""
    try:
        response = requests.get(API_URL, timeout=TIMEOUT)
        if response.status_code == 200:
            logger.info(f"✅ Ping exitoso - Status: {response.status_code}")
            return True
        else:
            logger.warning(f"⚠️ Ping con status inesperado: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Error en ping: {e}")
        return False

def main():
    """Función principal del script"""
    logger.info("🚀 Iniciando script de keep-alive para SWallet API")
    logger.info(f"📍 URL: {API_URL}")
    logger.info(f"⏰ Intervalo: {PING_INTERVAL} segundos ({PING_INTERVAL/60:.1f} minutos)")
    
    ping_count = 0
    
    while True:
        try:
            ping_count += 1
            logger.info(f"🔄 Ping #{ping_count} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            if ping_api():
                logger.info("✅ API respondiendo correctamente")
            else:
                logger.warning("⚠️ API no respondió correctamente")
            
            logger.info(f"😴 Esperando {PING_INTERVAL} segundos hasta el próximo ping...")
            time.sleep(PING_INTERVAL)
            
        except KeyboardInterrupt:
            logger.info("🛑 Script interrumpido por el usuario")
            break
        except Exception as e:
            logger.error(f"❌ Error inesperado: {e}")
            logger.info("🔄 Continuando en 5 minutos...")
            time.sleep(300)  # Esperar 5 minutos antes de reintentar

if __name__ == "__main__":
    main()
