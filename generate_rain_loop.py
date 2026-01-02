#!/usr/bin/env python3
"""
Genera un pequeño bucle de lluvia (2s @30fps) en `assets/video/rain_loop.mp4`.
El clip tiene fondo negro y trazos blancos (uso de blend screen en overlay reproducirá gotas visibles).
"""
from pathlib import Path
from PIL import Image, ImageDraw
import random
import subprocess

OUT = Path("assets/video/rain_loop.mp4")
TMP = Path("assets/video/rain_frames")
TMP.mkdir(parents=True, exist_ok=True)
FPS = 30
DURATION = 2
W, H = 1280, 720
FRAMES = FPS * DURATION
NUM_DROPS = 350

print("Generando frames de lluvia...")
# Initialize drops: (x, y, length, speed)
drops = []
for _ in range(NUM_DROPS):
    x = random.randint(0, W-1)
    y = random.randint(0, H)
    length = random.randint(6, 24)
    speed = random.uniform(4.0, 12.0)
    drops.append([x, y, length, speed])

for f in range(FRAMES):
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    for d in drops:
        x, y, length, speed = d
        # Draw a thin vertical streak with slight blur effect (multiple lines)
        y_int = int(y)
        draw.line((x, y_int, x, y_int + length), fill=(220, 220, 230), width=1)
        draw.line((x-1, y_int, x-1, y_int + length), fill=(200, 200, 210), width=1)
        # update position
        d[1] += speed
        if d[1] - length > H:
            d[0] = random.randint(0, W-1)
            d[1] = -random.randint(10, 200)
            d[2] = random.randint(6, 24)
            d[3] = random.uniform(4.0, 12.0)
    path = TMP / f"frame_{f:04d}.png"
    img.save(path, "PNG")

print("Encoding frames to MP4 (mpeg4 codec)...")
# Encode to mp4 (mpeg4 because libx264 not available)
ffmpeg = r"C:\Users\Admin\AppData\Local\Microsoft\WinGet\Packages\BtbN.FFmpeg.LGPL.Shared.8.0_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-n8.0.1-17-g27a297f186-win64-lgpl-shared-8.0\bin\ffmpeg.exe"
cmd = [
    ffmpeg,
    "-y",
    "-framerate", str(FPS),
    "-i", str(TMP / "frame_%04d.png"),
    "-c:v", "mpeg4", "-q:v", "5",
    "-r", str(FPS),
    str(OUT)
]
subprocess.run(cmd, check=True)
print(f"Generado: {OUT} ({OUT.stat().st_size/1024/1024:.2f} MB)")

# Cleanup frames
for p in TMP.glob("frame_*.png"):
    p.unlink()
TMP.rmdir()
print("Frames temporales eliminados.")
