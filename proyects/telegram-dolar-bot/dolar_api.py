import requests
from datetime import datetime

def get_dolar_api():
    url = "https://api.bluelytics.com.ar/v2/latest"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return {
            'fecha': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'oficial_venta': data['oficial']['value_sell'],
            'blue_venta': data['blue']['value_sell'],
            'blue_compra': data['blue']['value_buy']
        }
    except Exception as e:
        print(f"Error al obtener dólar: {e}")
        return None