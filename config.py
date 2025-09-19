#!/usr/bin/env python3
"""
Configuración para el script de keep-alive
"""

import os
from typing import List

class KeepAliveConfig:
    """Configuración para el script de keep-alive"""
    
    def __init__(self):
        # URL base de la API
        self.API_BASE_URL = os.getenv('API_BASE_URL', 'https://swallet-troe.onrender.com')
        
        # Endpoints a monitorear
        self.ENDPOINTS = [
            "/api",
            "/api/health", 
            "/api/info",
            "/api/users/stats"
        ]
        
        # Intervalo de ping en segundos (30 segundos por defecto)
        self.PING_INTERVAL = int(os.getenv('PING_INTERVAL', 30))
        
        # Timeout para las requests
        self.TIMEOUT = int(os.getenv('TIMEOUT', 30))
        
        # Número máximo de reintentos
        self.MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
        
        # Directorio de logs
        self.LOG_DIR = os.getenv('LOG_DIR', 'logs')
        
        # Nivel de logging
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
        
        # Modo de ejecución
        self.MODE = os.getenv('MODE', 'production')  # development, production
        
    def get_endpoints(self) -> List[str]:
        """Retorna la lista de endpoints a monitorear"""
        return self.ENDPOINTS
    
    def get_ping_interval(self) -> int:
        """Retorna el intervalo de ping en segundos"""
        return self.PING_INTERVAL
    
    def get_timeout(self) -> int:
        """Retorna el timeout para las requests"""
        return self.TIMEOUT
    
    def is_development(self) -> bool:
        """Retorna True si está en modo desarrollo"""
        return self.MODE == 'development'
    
    def get_log_level(self) -> str:
        """Retorna el nivel de logging"""
        return self.LOG_LEVEL

# Configuración por defecto
DEFAULT_CONFIG = KeepAliveConfig()

# Configuraciones predefinidas
CONFIGS = {
    'development': {
        'PING_INTERVAL': 5 * 60,  # 5 minutos
        'TIMEOUT': 10,
        'LOG_LEVEL': 'DEBUG',
        'ENDPOINTS': ['/api', '/api/health']
    },
    'production': {
        'PING_INTERVAL': 30,  # 30 segundos
        'TIMEOUT': 30,
        'LOG_LEVEL': 'INFO',
        'ENDPOINTS': ['/api', '/api/health', '/api/info', '/api/users/stats']
    },
    'aggressive': {
        'PING_INTERVAL': 30,  # 30 segundos
        'TIMEOUT': 20,
        'LOG_LEVEL': 'INFO',
        'ENDPOINTS': ['/api', '/api/health', '/api/info', '/api/users/stats']
    }
}

def get_config(mode: str = 'production') -> KeepAliveConfig:
    """Retorna la configuración para el modo especificado"""
    config = KeepAliveConfig()
    
    if mode in CONFIGS:
        config_data = CONFIGS[mode]
        config.PING_INTERVAL = config_data['PING_INTERVAL']
        config.TIMEOUT = config_data['TIMEOUT']
        config.LOG_LEVEL = config_data['LOG_LEVEL']
        config.ENDPOINTS = config_data['ENDPOINTS']
        config.MODE = mode
    
    return config
