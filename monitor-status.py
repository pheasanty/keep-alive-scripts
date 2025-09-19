#!/usr/bin/env python3
"""
Script para monitorear el estado de la API y el keep-alive
"""

import json
import requests
from datetime import datetime
from pathlib import Path
import sys

def load_status():
    """Carga el estado guardado del keep-alive"""
    status_file = Path("logs/api-status.json")
    if status_file.exists():
        try:
            with open(status_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error cargando estado: {e}")
            return None
    return None

def test_api_current():
    """Prueba la API actualmente"""
    try:
        response = requests.get("https://swallet-troe.onrender.com/api", timeout=10)
        return {
            "status_code": response.status_code,
            "response_time": response.elapsed.total_seconds(),
            "response_text": response.text[:100] + "..." if len(response.text) > 100 else response.text
        }
    except Exception as e:
        return {"error": str(e)}

def main():
    """Función principal de monitoreo"""
    print("🔍 Monitor de Estado - SWallet API")
    print("=" * 50)
    
    # Cargar estado guardado
    status = load_status()
    if status:
        print("📊 Estado Guardado:")
        print(f"   Último ping: {status.get('last_ping', 'N/A')}")
        print(f"   Total de pings: {status.get('ping_count', 'N/A')}")
        print(f"   Fallos consecutivos: {status.get('consecutive_failures', 'N/A')}")
        print(f"   Estado de la API: {status.get('api_status', 'N/A')}")
        print(f"   Modo: {status.get('mode', 'N/A')}")
        print()
    
    # Probar API actualmente
    print("🔄 Probando API actualmente...")
    current_test = test_api_current()
    
    if "error" in current_test:
        print(f"❌ Error: {current_test['error']}")
    else:
        print(f"✅ Status Code: {current_test['status_code']}")
        print(f"⏱️ Tiempo de respuesta: {current_test['response_time']:.2f} segundos")
        print(f"📝 Respuesta: {current_test['response_text']}")
    
    print()
    print("🎯 Endpoints monitoreados:")
    if status and 'endpoints' in status:
        for endpoint in status['endpoints']:
            print(f"   - {endpoint}")
    
    print()
    print("📁 Archivos de log:")
    log_dir = Path("logs")
    if log_dir.exists():
        for log_file in log_dir.glob("*.log"):
            print(f"   - {log_file}")
    else:
        print("   - No se encontró directorio de logs")

if __name__ == "__main__":
    main()
