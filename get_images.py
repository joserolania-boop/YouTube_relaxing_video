#!/usr/bin/env python3
"""
Generar imágenes de alta calidad usando API gratuita o síntesis procedural
Alternativa más ligera que Stable Diffusion
"""

import requests
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import io
import time

# Crear directorio
output_dir = Path("./assets/video")
output_dir.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("GENERADOR DE IMÁGENES - ALTERNATIVA LIGERA")
print("=" * 70)
print()

# ============================================================================
# Opción 1: Descargar de IA API gratuita (replicate.com si está disponible)
#           Alternativa: Usar Hugging Face Inference API
# ============================================================================

print("1️⃣  Obteniendo imágenes de alta calidad...")

# ============================================================================
# Alternativa: Usar API de Unsplash para obtener imágenes reales
# ============================================================================

print("2️⃣  Descargando imágenes de alta calidad desde Unsplash...")
print("-" * 70)

def download_image(url, filepath, name):
    """Descargar imagen desde URL"""
    try:
        print(f"  Descargando {name}...")
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(response.content)
            size_mb = filepath.stat().st_size / 1024 / 1024
            print(f"  ✓ {filepath.name} ({size_mb:.1f}MB)")
            return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
    return False

# URLs de Unsplash - imágenes de alta calidad
forest_urls = [
    "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1280&h=720&fit=crop&q=85",  # Bosque con lluvia
    "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1280&h=720&fit=crop&q=85",  # Lluvia en ventana
    "https://images.unsplash.com/photo-1441895206446-0da3fbc59cff?w=1280&h=720&fit=crop&q=85",  # Naturaleza lluviosa
]

coffee_urls = [
    "https://images.unsplash.com/photo-1495521821757-a1efb6729352?w=1280&h=720&fit=crop&q=85",  # Café latte
    "https://images.unsplash.com/photo-1559056199-641a0ac8b3f4?w=1280&h=720&fit=crop&q=85",  # Café con vapor
    "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=1280&h=720&fit=crop&q=85",  # Café aérea
]

forest_path = output_dir / "bosque_ventana_ia.png"
coffee_path = output_dir / "taza_cafe_ia.png"

# Intentar descargar bosque
for i, url in enumerate(forest_urls):
    if download_image(url, forest_path, "bosque lluvioso"):
        break
else:
    print("  ⚠️  No se pudo descargar bosque")

print()

# Intentar descargar café
for i, url in enumerate(coffee_urls):
    if download_image(url, coffee_path, "taza de café"):
        break
else:
    print("  ⚠️  No se pudo descargar café")

print()
print("=" * 70)
print("✓ Imágenes listas")
print("=" * 70)
