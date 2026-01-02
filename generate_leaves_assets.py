#!/usr/bin/env python3
"""
Genera bucles de hojas cayendo: `assets/video/leaves_light.mp4` y `assets/video/leaves_medium.mp4`.
Cada clip tiene fondo negro y hojas blancas (se combinarán con blend=screen para que se vean naturales).
"""
from pathlib import Path
from PIL import Image, ImageDraw
import random
import subprocess

OUT_DIR = Path("assets/video")
OUT_DIR.mkdir(parents=True, exist_ok=True)
FFMPEG = r"C:\Users\Admin\AppData\Local\Microsoft\WinGet\Packages\BtbN.FFmpeg.LGPL.Shared.8.0_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-n8.0.1-17-g27a297f186-win64-lgpl-shared-8.0\bin\ffmpeg.exe"
W, H = 1280, 720
FPS = 30
DURATION = 2
FRAMES = FPS * DURATION

configs = [
    ("leaves_light.mp4", 40, (8, 20), (30, 60), (220, 190, 120)),
    ("leaves_medium.mp4", 28, (12, 30), (20, 50), (200, 160, 100)),
]

def gen(name, num_leaves, size_range, speed_range, color):
    tmp = OUT_DIR / (name + "_frames")
    tmp.mkdir(exist_ok=True)
    leaves = []
    for _ in range(num_leaves):
        x = random.randint(0, W)
        y = random.randint(-H, H)
        size = random.randint(*size_range)
        speed = random.uniform(*speed_range)
        rot = random.uniform(0, 360)
        leaves.append([x, y, size, speed, rot])

    for f in range(FRAMES):
        img = Image.new('RGB', (W, H), (0, 0, 0))
        draw = ImageDraw.Draw(img)
        for l in leaves:
            x, y, size, speed, rot = l
            y = int(y)
            # draw oval leaf with slight slant
            bbox = [x, y, x + size, y + int(size*0.6)]
            draw.ellipse(bbox, fill=tuple(color))
            # update position with drift
            l[1] += speed
            l[0] += int(5 * random.uniform(-1, 1))
            l[4] += random.uniform(-5, 5)
            if l[1] - size > H:
                l[0] = random.randint(0, W)
                l[1] = -random.randint(10, 200)
                l[2] = random.randint(*size_range)
                l[3] = random.uniform(*speed_range)
        path = tmp / f"frame_{f:04d}.png"
        img.save(path, 'PNG')

    out = OUT_DIR / name
    cmd = [FFMPEG, '-y', '-framerate', str(FPS), '-i', str(tmp / 'frame_%04d.png'), '-c:v', 'mpeg4', '-q:v', '5', '-r', str(FPS), str(out)]
    subprocess.run(cmd, check=True)
    # cleanup
    for p in tmp.glob('frame_*.png'):
        p.unlink()
    tmp.rmdir()
    print(f"Generado {out} ({out.stat().st_size/1024/1024:.2f} MB)")

for c in configs:
    gen(*c)
