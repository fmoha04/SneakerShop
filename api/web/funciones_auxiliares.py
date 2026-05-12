import decimal
import json
import html
import bleach 

def sanitize_field(data):
    if isinstance(data, str):
        return bleach.clean(html.escape(data))
    if isinstance(data, dict):
        return {k: sanitize_field(v) for k, v in data.items()}
    if isinstance(data, list):
        return [sanitize_field(v) for v in data]
    return data

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal): return float(obj)

def calculariva(precio):
    return precio * 0.21


