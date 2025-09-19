#!/usr/bin/env python3
"""
Script de ping constante para SWallet API - Optimizado para Render
Hace ping cada 30 segundos para mantener la API activa
"""

import requests
import time
import logging
import json
import sys
import os
import signal
from datetime import datetime
from pathlib import Path

class SWalletPingConstant:
    """Clase para mantener activa la API de SWallet con ping constante"""
    
    def __init__(self):
        self.api_url = "https://swallet-troe.onrender.com"
        self.endpoints = ['/api', '/api/health', '/api/info']
        self.ping_interval = 30  # 30 segundos
        self.timeout = 30
        self.log_dir = Path("logs")
        self.log_dir.mkdir(exist_ok=True)
        
        self.ping_count = 0
        self.consecutive_failures = 0
        self.running = True
        
        self._setup_logging()
        self._setup_signal_handlers()
    
    def _setup_logging(self):
        """Configura el sistema de logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_dir / 'swallet-ping.log', encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger(__name__)
    
    def _setup_signal_handlers(self):
        """Configura los manejadores de señales para cierre graceful"""
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Manejador de señales para cierre graceful"""
        self.logger.info("Recibida señal de cierre, deteniendo script...")
        self.running = False
    
    def ping_endpoint(self, endpoint):
        """Hace un ping a un endpoint específico"""
        url = f"{self.api_url}{endpoint}"
        try:
            response = requests.get(url, timeout=self.timeout)
            if response.status_code == 200:
                self.logger.info(f"OK {endpoint} - Status: {response.status_code}")
                return True
            else:
                self.logger.warning(f"WARNING {endpoint} - Status: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.logger.error(f"ERROR {endpoint} - Error: {e}")
            return False
    
    def ping_all_endpoints(self):
        """Hace ping a todos los endpoints configurados"""
        self.logger.info("Iniciando ping a todos los endpoints...")
        successful_pings = 0
        
        for endpoint in self.endpoints:
            if self.ping_endpoint(endpoint):
                successful_pings += 1
            time.sleep(1)  # Pequeña pausa entre pings
        
        self.logger.info(f"Resultado: {successful_pings}/{len(self.endpoints)} endpoints respondieron correctamente")
        return successful_pings > 0
    
    def save_status(self):
        """Guarda el estado actual en un archivo JSON"""
        status_data = {
            "last_ping": datetime.now().isoformat(),
            "ping_count": self.ping_count,
            "consecutive_failures": self.consecutive_failures,
            "api_status": "healthy" if self.consecutive_failures == 0 else "degraded",
            "endpoints": self.endpoints,
            "ping_interval": self.ping_interval,
            "api_url": self.api_url
        }
        
        status_file = self.log_dir / "swallet-ping-status.json"
        try:
            with open(status_file, 'w', encoding='utf-8') as f:
                json.dump(status_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error guardando estado: {e}")
    
    def run(self):
        """Ejecuta el loop principal del ping constante"""
        self.logger.info("=== SWALLET PING CONSTANTE ===")
        self.logger.info(f"URL Base: {self.api_url}")
        self.logger.info(f"Endpoints: {', '.join(self.endpoints)}")
        self.logger.info(f"Intervalo: {self.ping_interval} segundos ({self.ping_interval/60:.1f} minutos)")
        self.logger.info("Presiona Ctrl+C para detener el script")
        self.logger.info("=" * 50)
        
        while self.running:
            try:
                self.ping_count += 1
                current_time = datetime.now()
                
                self.logger.info(f"Ping #{self.ping_count} - {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Hacer ping a todos los endpoints
                if self.ping_all_endpoints():
                    self.consecutive_failures = 0
                    self.logger.info("API funcionando correctamente")
                else:
                    self.consecutive_failures += 1
                    self.logger.warning(f"API con problemas - Fallos consecutivos: {self.consecutive_failures}")
                
                # Guardar estado
                self.save_status()
                
                # Si hay muchos fallos consecutivos, esperar menos tiempo
                if self.consecutive_failures >= 3:
                    wait_time = 5 * 60  # 5 minutos
                    self.logger.warning(f"Muchos fallos consecutivos, esperando solo {wait_time/60:.1f} minutos...")
                else:
                    wait_time = self.ping_interval
                
                self.logger.info(f"Esperando {wait_time} segundos hasta el próximo ping...")
                self.logger.info("-" * 50)
                
                # Esperar con posibilidad de interrupción
                for _ in range(wait_time):
                    if not self.running:
                        break
                    time.sleep(1)
                
            except Exception as e:
                self.logger.error(f"Error inesperado: {e}")
                self.logger.info("Continuando en 5 minutos...")
                for _ in range(300):  # 5 minutos
                    if not self.running:
                        break
                    time.sleep(1)
        
        self.logger.info("Script detenido")

def main():
    """Función principal"""
    print("=== SWALLET PING CONSTANTE ===")
    print("Mantiene activa tu API en Render")
    print("URL: https://swallet-troe.onrender.com")
    print("Intervalo: 30 segundos")
    print("=" * 50)
    
    # Crear y ejecutar el ping constante
    ping_constant = SWalletPingConstant()
    ping_constant.run()

if __name__ == "__main__":
    main()
