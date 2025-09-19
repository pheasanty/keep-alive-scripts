#!/usr/bin/env python3
"""
Script principal de keep-alive para SWallet API (Sin emojis para compatibilidad con Windows)
Combina todas las funcionalidades en un solo script
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

class SWalletKeepAlive:
    """Clase principal para mantener activa la API de SWallet"""
    
    def __init__(self, mode='production'):
        self.mode = mode
        self.api_url = "https://swallet-troe.onrender.com"
        self.endpoints = self._get_endpoints()
        self.ping_interval = self._get_ping_interval()
        self.timeout = self._get_timeout()
        self.log_dir = Path("logs")
        self.log_dir.mkdir(exist_ok=True)
        
        self.ping_count = 0
        self.consecutive_failures = 0
        self.running = True
        
        self._setup_logging()
        self._setup_signal_handlers()
    
    def _get_endpoints(self):
        """Retorna los endpoints según el modo"""
        if self.mode == 'development':
            return ['/api', '/api/health']
        elif self.mode == 'aggressive':
            return ['/api', '/api/health', '/api/info', '/api/users/stats']
        else:  # production
            return ['/api', '/api/health', '/api/info', '/api/users/stats']
    
    def _get_ping_interval(self):
        """Retorna el intervalo de ping según el modo"""
        if self.mode == 'development':
            return 5 * 60  # 5 minutos
        elif self.mode == 'aggressive':
            return 15 * 60  # 15 minutos
        else:  # production
            return 25 * 60  # 25 minutos
    
    def _get_timeout(self):
        """Retorna el timeout según el modo"""
        if self.mode == 'development':
            return 10
        else:
            return 30
    
    def _setup_logging(self):
        """Configura el sistema de logging"""
        log_level = logging.DEBUG if self.mode == 'development' else logging.INFO
        
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_dir / 'swallet-keep-alive.log', encoding='utf-8'),
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
            time.sleep(2)  # Pequeña pausa entre pings
        
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
            "mode": self.mode,
            "config": {
                "ping_interval": self.ping_interval,
                "timeout": self.timeout,
                "api_url": self.api_url
            }
        }
        
        status_file = self.log_dir / "swallet-status.json"
        try:
            with open(status_file, 'w', encoding='utf-8') as f:
                json.dump(status_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error guardando estado: {e}")
    
    def run(self):
        """Ejecuta el loop principal del keep-alive"""
        self.logger.info("Iniciando SWallet Keep-Alive")
        self.logger.info(f"URL Base: {self.api_url}")
        self.logger.info(f"Endpoints: {', '.join(self.endpoints)}")
        self.logger.info(f"Intervalo: {self.ping_interval} segundos ({self.ping_interval/60:.1f} minutos)")
        self.logger.info(f"Modo: {self.mode}")
        
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
    # Obtener modo desde argumentos
    mode = sys.argv[1] if len(sys.argv) > 1 else 'production'
    
    if mode not in ['development', 'production', 'aggressive']:
        print("Modo inválido. Usa: development, production, o aggressive")
        sys.exit(1)
    
    # Crear y ejecutar el keep-alive
    keep_alive = SWalletKeepAlive(mode)
    keep_alive.run()

if __name__ == "__main__":
    main()
