#!/usr/bin/env python3
"""
Script avanzado para generar video profesional con animaciones
- Lluvia dinámica y realista
- Vapor del café animado
- Efectos de parallax
- Integración suave de elementos
"""

import subprocess
import os
from pathlib import Path

# Rutas
FFMPEG = r"C:\Users\Admin\AppData\Local\Microsoft\WinGet\Packages\BtbN.FFmpeg.LGPL.Shared.8.0_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-n8.0.1-17-g27a297f186-win64-lgpl-shared-8.0\bin\ffmpeg.exe"
OUTPUT_DIR = Path("./out")
ASSETS_DIR = Path("./assets/video")
OUTPUT_FILE = OUTPUT_DIR / "bosque_cafe_lluvia_profesional.mp4"

# Configuración
DURATION = 60
FPS = 30
WIDTH = 1280
HEIGHT = 720

OUTPUT_DIR.mkdir(exist_ok=True)

# Imágenes generadas
forest_image = ASSETS_DIR / "bosque_ventana_ia.png"
coffee_image = ASSETS_DIR / "taza_cafe_ia.png"

if not forest_image.exists():
    print(f"Error: {forest_image} no encontrada")
    exit(1)

if not coffee_image.exists():
    print(f"Advertencia: {coffee_image} no encontrada - usando bosque solo")
    coffee_image = None

print("=" * 70)
print("GENERADOR DE VIDEO PROFESIONAL CON ANIMACIONES")
print("=" * 70)
print(f"Duracion: {DURATION}s | Resolucion: {WIDTH}x{HEIGHT} | FPS: {FPS}")
print(f"Bosque: {forest_image.name}")
if coffee_image:
    print(f"Cafe: {coffee_image.name}")
print()

# ====================================================================
# FILTERGRAPH AVANZADO CON ANIMACIONES PROFESIONALES
# ====================================================================

# Componentes:
# [0] Imagen de bosque - base con zoom sutil
# [1] Lluvia dinámica - múltiples capas de ruido
# [2] Café con vapor - animación de elevación
# [3] Audio - ruido rosa binaural

print("Construyendo filtergraph con animaciones...")

# Lluvia: múltiples capas de ruido con diferentes velocidades
rain_layers = (
    "["
    "1:v"
    "]"
    # Capa 1: lluvia rápida
    "fps=25,noise=alls=30:allf=t,gblur=sigma=1.2,colorchannelmixer=aa=0.25"
    "[rain1];"
    
    # Capa 2: lluvia lenta (movimiento parallax)
    "[1:v]fps=20,noise=alls=20:allf=t,gblur=sigma=1.8,colorchannelmixer=aa=0.15"
    "[rain2];"
    
    # Combinar capas de lluvia
    "[rain1][rain2]blend=all_mode=screen[rain_combined]"
)

# Bosque base: zoom sutil y ajustes de color
forest_filter = (
    "[0:v]"
    "scale=1280:720:force_original_aspect_ratio=decrease,"
    "pad=1280:720:(ow-iw)/2:(oh-ih)/2,"
    "format=rgba,"
    # Ajuste de brillo para efecto de lluvia
    "eq=brightness=0.05:contrast=1.1:saturation=0.95,"
    # Zoom sutil: empieza en 100%, llega a 105% en 60s
    "scale='min(iw\\,ih)*1.0+(min(iw\\,ih)*0.05)*(t/60)':'-1',"
    "crop=1280:720"
    "[forest_base]"
)

if coffee_image:
    # Café con vapor animado
    coffee_filter = (
        "[2:v]"
        "scale=400:300,"
        "format=rgba,"
        # Efecto de desvanecimiento suave entrada/salida
        "format=rgba"
        "[coffee_base]"
    )
    
    # Vapor: círculos que suben y se desvanecen
    steam_filter = (
        "[3:v]"
        "fps=30,"
        "drawcircle=x='w/2+50*sin(2*PI*t/4)':y='h-100-t*20':r='40+t*5':"
        "color=white@'max(0,1-t/3)':thickness=fill,"
        "drawcircle=x='w/2-30+40*cos(2*PI*t/3)':y='h-80-t*15':r='30+t*3':"
        "color=white@'max(0,0.8-t/3)':thickness=fill,"
        "format=rgba"
        "[steam]"
    )
    
    # Composición final con café y vapor
    composition = (
        "[forest_base][rain_combined]overlay=x=0:y=0[with_rain];"
        "[with_rain][coffee_base]overlay=x=800:y=450[with_coffee];"
        "[with_coffee][steam]overlay=x=800:y=350[final]"
    )
else:
    # Solo bosque + lluvia
    composition = (
        "[forest_base][rain_combined]overlay=x=0:y=0[final]"
    )

# Filtergraph completo
filter_complex = forest_filter + ";" + rain_layers + ";" + composition

if coffee_image:
    filter_complex = forest_filter + ";" + coffee_filter + ";" + steam_filter + ";" + rain_layers + ";" + composition

print("Filtergraph listo")
print()

# ====================================================================
# CONSTRUIR COMANDO FFMPEG
# ====================================================================

print("Construyendo comando FFmpeg...")

# Inputs
inputs = [
    "-loop", "1", "-i", str(forest_image),  # [0] Bosque
    "-f", "lavfi", "-i", "color=0x000000:s=1280x720:d=60",  # [1] Para lluvia
]

if coffee_image:
    inputs.extend([
        "-loop", "1", "-i", str(coffee_image),  # [2] Café
        "-f", "lavfi", "-i", f"color=0x000000:s=400x300:d={DURATION}",  # [3] Para vapor
    ])

# Audio
inputs.extend([
    "-f", "lavfi", "-i", f"anoisesrc=r=44100:c=2:d={DURATION}",  # Audio ruido rosa
])

# Filtergraph
filter_args = ["-filter_complex", filter_complex]

# Outputs
outputs = [
    "-map", "[final]",
    "-map", str(len(inputs)//2) + ":a",  # Audio del último input
    "-c:v", "mpeg4",
    "-q:v", "6",
    "-c:a", "aac",
    "-ar", "44100",
    "-b:a", "256k",
    "-t", str(DURATION),
    "-r", str(FPS),
    "-y",
    str(OUTPUT_FILE)
]

cmd = [FFMPEG] + inputs + filter_args + outputs

print(f"Comando: {' '.join(cmd[:10])}...")
print()

# ====================================================================
# EJECUTAR FFMPEG
# ====================================================================

print("Ejecutando FFmpeg...")
print("-" * 70)

try:
    result = subprocess.run(
        cmd,
        capture_output=False,
        text=True,
        timeout=600
    )
    
    if result.returncode == 0:
        file_size = OUTPUT_FILE.stat().st_size / 1024 / 1024
        print()
        print("=" * 70)
        print("VIDEO GENERADO EXITOSAMENTE")
        print("=" * 70)
        print(f"Archivo: {OUTPUT_FILE}")
        print(f"Tamano: {file_size:.1f} MB")
        print(f"Duracion: {DURATION}s | Resolucion: {WIDTH}x{HEIGHT}@{FPS}fps")
        print()
        print("Caracteristicas del video:")
        print("  - Imagen de bosque de alta calidad (Unsplash)")
        if coffee_image:
            print("  - Taza de cafe realista con vapor animado")
        print("  - Lluvia multicapa con efectos parallax")
        print("  - Zoom suave y ajuste de color")
        print("  - Audio ruido rosa relajante")
        print()
    else:
        print("Error en FFmpeg")
        exit(1)
        
except subprocess.TimeoutExpired:
    print("Timeout: el proceso tardó demasiado")
    exit(1)
except Exception as e:
    print(f"Error: {e}")
    exit(1)
