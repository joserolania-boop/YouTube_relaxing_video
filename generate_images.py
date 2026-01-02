#!/usr/bin/env python3
"""
Generar imágenes de alta calidad usando Stable Diffusion
- Bosque lluvioso con ventana
- Taza de café realista
"""

import os
from pathlib import Path
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
import torch
from PIL import Image

# Crear directorio de salida
output_dir = Path("./assets/video")
output_dir.mkdir(parents=True, exist_ok=True)

# Configuración
model_id = "stabilityai/stable-diffusion-2-1"
device = "cpu"  # Usar CPU si no hay GPU
dtype = torch.float32

print("=" * 60)
print("GENERADOR DE IMÁGENES CON IA - Stable Diffusion 2.1")
print("=" * 60)
print(f"Dispositivo: {device}")
print(f"Modelo: {model_id}")
print()

# ============================================================
# GENERAR IMAGEN: BOSQUE LLUVIOSO DESDE VENTANA
# ============================================================

print("1️⃣  Generando imagen de BOSQUE LLUVIOSO...")
print("-" * 60)

try:
    pipe_forest = StableDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=dtype,
        safety_checker=None,
    ).to(device)
    
    pipe_forest.scheduler = DPMSolverMultistepScheduler.from_config(
        pipe_forest.scheduler.config
    )
    
    prompt_forest = (
        "A serene view of a lush green forest with heavy rain falling outside a wooden window frame. "
        "Raindrops on the glass, misty atmosphere, soft natural lighting, moody ambiance, "
        "photorealistic, 4K, professional photography, cozy indoor perspective looking out. "
        "Dense trees, wet leaves, peaceful and calming, high quality"
    )
    
    negative_prompt = (
        "blurry, low quality, distorted, ugly, bad anatomy, "
        "people, humans, text, watermark, logo"
    )
    
    print(f"Prompt: {prompt_forest[:80]}...")
    print("Generando... (esto puede tomar 2-3 minutos)")
    
    with torch.no_grad():
        image_forest = pipe_forest(
            prompt=prompt_forest,
            negative_prompt=negative_prompt,
            height=720,
            width=1280,
            num_inference_steps=20,
            guidance_scale=7.5,
            num_images_per_prompt=1,
        ).images[0]
    
    forest_path = output_dir / "bosque_ventana_ia.png"
    image_forest.save(forest_path)
    print(f"✓ Imagen guardada: {forest_path}")
    print(f"  Tamaño: {image_forest.size}")
    print()
    
except Exception as e:
    print(f"✗ Error generando bosque: {e}")
    print()

# ============================================================
# GENERAR IMAGEN: TAZA DE CAFÉ REALISTA
# ============================================================

print("2️⃣  Generando imagen de TAZA DE CAFÉ...")
print("-" * 60)

try:
    pipe_coffee = StableDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=dtype,
        safety_checker=None,
    ).to(device)
    
    pipe_coffee.scheduler = DPMSolverMultistepScheduler.from_config(
        pipe_coffee.scheduler.config
    )
    
    prompt_coffee = (
        "A beautiful ceramic coffee mug with hot coffee, steam rising up, "
        "sitting on a wooden table, warm lighting, cozy atmosphere, "
        "photorealistic, 4K, professional product photography, "
        "soft shadows, warm brown tones, morning light, high quality, detailed"
    )
    
    print(f"Prompt: {prompt_coffee[:80]}...")
    print("Generando... (esto puede tomar 2-3 minutos)")
    
    with torch.no_grad():
        image_coffee = pipe_coffee(
            prompt=prompt_coffee,
            negative_prompt=negative_prompt,
            height=720,
            width=1280,
            num_inference_steps=20,
            guidance_scale=7.5,
            num_images_per_prompt=1,
        ).images[0]
    
    coffee_path = output_dir / "taza_cafe_ia.png"
    image_coffee.save(coffee_path)
    print(f"✓ Imagen guardada: {coffee_path}")
    print(f"  Tamaño: {image_coffee.size}")
    print()
    
except Exception as e:
    print(f"✗ Error generando café: {e}")
    print()

print("=" * 60)
print("✓ Generación de imágenes completada")
print("=" * 60)
print()
print("Siguiente paso: Crear video con animaciones")
