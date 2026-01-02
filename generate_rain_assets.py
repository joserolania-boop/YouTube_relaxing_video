#!/usr/bin/env python3
"""
Genera tres bucles de lluvia distintos: rain_light.mp4, rain_medium.mp4, rain_heavy.mp4
Cada uno tiene parámetros ajustados para velocidad, longitud e intensidad.
"""
from pathlib import Path
import subprocess
import random
from PIL import Image, ImageDraw

FFMPEG = r"C:\Users\Admin\AppData\Local\Microsoft\WinGet\Packages\BtbN.FFmpeg.LGPL.Shared.8.0_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-n8.0.1-17-g27a297f186-win64-lgpl-shared-8.0\bin\ffmpeg.exe"
OUT_DIR = Path("assets/video")
OUT_DIR.mkdir(parents=True, exist_ok=True)
W,H=1280,720
FPS=30
DURATION=2
FRAMES=FPS*DURATION

configs = [
    ("rain_light.mp4", 700, (12,30), (10.0,22.0), (240,240,250)),
    ("rain_medium.mp4", 500, (18,40), (7.0,16.0), (230,230,240)),
    ("rain_heavy.mp4", 350, (30,70), (6.0,12.0), (210,210,220)),
]

def gen(name, num_drops, length_range, speed_range, color):
    tmp = OUT_DIR / (name + "_frames")
    tmp.mkdir(exist_ok=True)
    drops=[]
    for _ in range(num_drops):
        x=random.randint(0,W-1)
        y=random.randint(0,H)
        length=random.randint(*length_range)
        speed=random.uniform(*speed_range)
        drops.append([x,y,length,speed])
    for f in range(FRAMES):
        img=Image.new('RGB',(W,H),(0,0,0))
        draw=ImageDraw.Draw(img)
        for d in drops:
            x,y,length,speed=d
            y_int=int(y)
            # draw a streak with a slight trail (multiple segments with decreasing brightness)
            for k in range(0, length, 3):
                alpha = int(255 * max(0.1, 1 - (k/length)))
                col = (min(255, color[0] + k//2), min(255, color[1] + k//2), min(255, color[2] + k//2))
                draw.line((x, y_int+k, x, y_int+min(length, k+3)), fill=col, width=1)
            d[1]+=speed
            if d[1]-length>H:
                d[0]=random.randint(0,W-1)
                d[1]=-random.randint(10,200)
                d[2]=random.randint(*length_range)
                d[3]=random.uniform(*speed_range)
        img.save(tmp/f"frame_{f:04d}.png")
    # encode
    out=OUT_DIR/name
    cmd=[FFMPEG,"-y","-framerate",str(FPS),"-i",str(tmp/"frame_%04d.png"),"-c:v","mpeg4","-q:v","5","-r",str(FPS),str(out)]
    subprocess.run(cmd, check=True)
    # cleanup
    for p in tmp.glob("frame_*.png"):
        p.unlink()
    tmp.rmdir()
    print(f"Generado {out} ({out.stat().st_size/1024/1024:.2f} MB)")

for cfg in configs:
    gen(*cfg)
