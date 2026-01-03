#!/usr/bin/env python3
"""Genera overlays: particles.webm, leaves_back.webm, leaves_front.webm
Simple procedural generator: dots for particles, ellipses for leaves with alpha and motion.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import random, os, subprocess, shutil, math

OUT_DIR = Path('assets/video')
OUT_DIR.mkdir(parents=True, exist_ok=True)
FPS = 30
DURATION = 8  # seconds for each loop
W, H = 1280, 720

FFMPEG = r"C:\Users\Admin\AppData\Local\Microsoft\WinGet\Packages\BtbN.FFmpeg.LGPL.Shared.8.0_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-n8.0.1-17-g27a297f186-win64-lgpl-shared-8.0\bin\ffmpeg.exe"

def ffmpeg_encode(frames_dir, out_path, fps=FPS):
    cmd = [
        FFMPEG,'-y','-f','image2','-framerate',str(fps),'-i', str(frames_dir / 'frame_%04d.png'),
        '-c:v','libvpx-vp9','-pix_fmt','yuva420p','-auto-alt-ref','0','-row-mt','1','-crf','28','-b:v','0',
        str(out_path)
    ]
    subprocess.run(cmd, check=True)

# 1) Particles
print('Generando particles.webm...')
par_dir = OUT_DIR / 'particles_frames'
if par_dir.exists(): shutil.rmtree(par_dir)
par_dir.mkdir()
num_frames = FPS * DURATION
particles = []
for i in range(120):
    # initialize particles: x,y, vx, vy, radius, alpha, life
    particles.append({
        'x': random.uniform(0, W),
        'y': random.uniform(0, H),
        'vx': random.uniform(-6,6) * 0.12,
        'vy': random.uniform(-10, -1) * 0.4,
        'r': random.uniform(2,8),
        'a': random.uniform(80,220),
        'phase': random.uniform(0,6.28)
    })

for f in range(num_frames):
    im = Image.new('RGBA',(W,H),(0,0,0,0))
    draw = ImageDraw.Draw(im)
    t = f / FPS
    for p in particles:
        # simple bobbing motion
        p['x'] += p['vx']
        p['y'] += p['vy'] + 0.3 * math.sin(p['phase'] + t*0.2)
        # respawn if out of bounds
        if p['y'] < -20 or p['x'] < -20 or p['x'] > W+20:
            p['x'] = random.uniform(-40, W+40)
            p['y'] = H + random.uniform(0, 60)
            p['vy'] = random.uniform(-10, -1) * 0.4
        alpha = max(20, min(255, int(p['a'] * (0.7 + 0.3*math.sin(t + p['phase'])))))
        bbox = [int(p['x']-p['r']), int(p['y']-p['r']), int(p['x']+p['r']), int(p['y']+p['r'])]
        draw.ellipse(bbox, fill=(255,255,220, alpha))
    im = im.filter(ImageFilter.GaussianBlur(radius=1.2))
    im.save(par_dir / f'frame_{f:04d}.png')

ffmpeg_encode(par_dir, OUT_DIR / 'particles.webm')
shutil.rmtree(par_dir)
print('particles.webm generado')

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--no-leaves', action='store_true', help='Generate only particles and skip leaves')
    args = p.parse_args()
else:
    # default when imported
    args = type('X', (), {'no_leaves': False})()

# 2) Leaves (back)
if not args.no_leaves:
    print('Generando leaves_back.webm y leaves_front.webm...')
for tag in ('back','front'):
    frames_dir = OUT_DIR / f'leaves_{tag}_frames'
    if frames_dir.exists(): shutil.rmtree(frames_dir)
    frames_dir.mkdir()
    num_leaves = 8 if tag=='back' else 14
    leaves = []
    for i in range(num_leaves):
        leaves.append({
            'x': random.uniform(0, W),
            'y': random.uniform(-H, H),
            'vx': random.uniform(-30,30) * (0.02 if tag=='back' else 0.06),
            'vy': random.uniform(20,80) * (0.02 if tag=='back' else 0.06),
            'r': random.uniform(24,70) * (0.8 if tag=='back' else 1.2),
            'rot': random.uniform(0,360),
            'drot': random.uniform(-30,30) * (0.1 if tag=='back' else 0.4),
            'color': (random.randint(160,220), random.randint(90,150), random.randint(30,70)),
            'alpha': 180 if tag=='back' else 230
        })
    for f in range(num_frames):
        im = Image.new('RGBA',(W,H),(0,0,0,0))
        for l in leaves:
            l['x'] += l['vx'] * (1 + 0.1*math.sin(f*0.1 + l['rot']))
            l['y'] += l['vy']
            l['rot'] = (l['rot'] + l['drot']*0.02) % 360
            # respawn
            if l['y'] > H + 50 or l['x'] < -100 or l['x'] > W + 100:
                l['x'] = random.uniform(-40, W+40)
                l['y'] = -random.uniform(0, 120)
        # draw leaves
        for l in leaves:
            leaf = Image.new('RGBA',(int(l['r']*1.6), int(l['r']*1.0)), (0,0,0,0))
            d = ImageDraw.Draw(leaf)
            # simple leaf ellipse
            bbox = [0, int(l['r']*0.1), int(l['r']*1.6), int(l['r']*0.9)]
            d.ellipse(bbox, fill=(l['color'][0], l['color'][1], l['color'][2], l['alpha']))
            # rotate and paste
            leaf = leaf.rotate(l['rot'], resample=Image.BICUBIC, expand=True)
            im.alpha_composite(leaf, dest=(int(l['x']), int(l['y'])))
        # slight blur for back layer
        if tag == 'back':
            im = im.filter(ImageFilter.GaussianBlur(radius=2.2))
        else:
            im = im.filter(ImageFilter.GaussianBlur(radius=0.4))
        im.save(frames_dir / f'frame_{f:04d}.png')
    out_name = OUT_DIR / f'leaves_{tag}.webm'
    ffmpeg_encode(frames_dir, out_name)
    shutil.rmtree(frames_dir)
print('Hojas generadas')

print('Todos los assets generados: particles + leaves')
