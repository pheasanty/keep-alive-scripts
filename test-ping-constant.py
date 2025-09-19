#!/usr/bin/env python3
"""
Script de prueba para el ping constante
"""

import requests
import time
from datetime import datetime

API_URL = "https://swallet-troe.onrender.com"
ENDPOINTS = ['/api', '/api/health', '/api/info']

def test_all_endpoints():
    """Prueba todos los endpoints"""
    print("=== PRUEBA DE PING CONSTANTE ===")
    print(f"URL Base: {API_URL}")
    print(f"Endpoints: {', '.join(ENDPOINTS)}")
    print(f"Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    successful_pings = 0
    
    for endpoint in ENDPOINTS:
        url = f"{API_URL}{endpoint}"
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                print(f"OK {endpoint} - Status: {response.status_code}")
                successful_pings += 1
            else:
                print(f"WARNING {endpoint} - Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"ERROR {endpoint} - Error: {e}")
        
        time.sleep(1)  # Pequeña pausa entre pings
    
    print("-" * 50)
    print(f"Resultado: {successful_pings}/{len(ENDPOINTS)} endpoints respondieron correctamente")
    
    if successful_pings == len(ENDPOINTS):
        print("API funcionando perfectamente!")
        return True
    else:
        print("API con problemas")
        return False

if __name__ == "__main__":
    test_all_endpoints()
