#!/usr/bin/env python3
"""
Script de prueba rápida para verificar la conectividad con la API (Sin emojis)
"""

import requests
import time
from datetime import datetime

API_URL = "https://swallet-troe.onrender.com/api"

def test_api():
    """Prueba la conectividad con la API"""
    print(f"Probando conectividad con: {API_URL}")
    print(f"Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    try:
        response = requests.get(API_URL, timeout=30)
        print(f"OK Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        print(f"Tiempo de respuesta: {response.elapsed.total_seconds():.2f} segundos")
        return True
    except requests.exceptions.RequestException as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    test_api()
