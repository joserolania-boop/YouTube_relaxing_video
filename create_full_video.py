#!/usr/bin/env python3
"""
Video Profesional Completo: Bosque Brumoso + Lluvia + Musica + Mensajes Motivadores
"""

import subprocess
from pathlib import Path
import json

# Configuración
FFMPEG = r"C:\Users\Admin\AppData\Local\Microsoft\WinGet\Packages\BtbN.FFmpeg.LGPL.Shared.8.0_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-n8.0.1-17-g27a297f186-win64-lgpl-shared-8.0\bin\ffmpeg.exe"
FOREST = Path("./assets/video/bosque_brumoso.jpg")
OUTPUT = Path("./out/bosque_completo_final.mp4")
AUDIO_FILE = Path("./assets/audio/ambient_music.mp3")
DURATION = 30
FPS = 30

# Crear directorio
OUTPUT.parent.mkdir(exist_ok=True)

print("=" * 70)
print("VIDEO PROFESIONAL: Bosque + Lluvia + Musica + Mensajes")
print("=" * 70)
print()

# ===== 1. DESCARGAR MUSICA ROYALTY-FREE =====
print("1. Descargando musica ambiental relajante...")

if not AUDIO_FILE.parent.exists():
    AUDIO_FILE.parent.mkdir(parents=True, exist_ok=True)

if not AUDIO_FILE.exists():
    import requests
    # Prefer open/royalty-free ambient music (Pixabay) — fallback to one other Pixabay track
    candidates = [
        "https://cdn.pixabay.com/download/audio/2022/03/10/audio_0475aeb10b.mp3",  # calm ambient (Pixabay)
        "https://cdn.pixabay.com/download/audio/2021/10/29/audio_5f0d9d5f7f.mp3"   # backup (Pixabay)
    ]
    downloaded = False
    for url in candidates:
        try:
            print(f"  Intentando descargar: {url.split('/')[-1]}...", end=" ")
            resp = requests.get(url, timeout=20)
            if resp.status_code == 200 and len(resp.content) > 1000:
                with open(AUDIO_FILE, 'wb') as f:
                    f.write(resp.content)
                size_mb = AUDIO_FILE.stat().st_size / 1024 / 1024
                print(f"OK ({size_mb:.1f}MB)")
                downloaded = True
                break
            else:
                print("falló")
        except Exception as e:
            print("error:", e)
    if not downloaded:
        print("  No se pudo descargar pista, usando anoisesrc como fallback")
        AUDIO_FILE = None

print()

# ===== 2. CONSTRUIR FILTERGRAPH =====
print("2. Construyendo filtergraph con lluvia multicapa + mensajes...")
print()

# Mensajes motivadores (aparecen cada 15 segundos - simplificados)
messages = [
    ("Respira", 0, 3),
    ("Paz", 15, 18),
    ("Presente", 30, 33),
    ("Cree", 45, 48),
]

# Generar filtros de texto (drawtext) - versión simplificada
text_filter_chain = ""
for msg, start, end in messages:
    if text_filter_chain:
        text_filter_chain += ","
    # Escaping simplificado para Windows/FFmpeg
    text_filter_chain += (
        f"drawtext=fontsize=36:fontcolor=white@0.8:text={msg}:"
        f"x=(w-text_w)/2:y=h-80:enable='between(t,{start},{end})'"
    )

# Filtergraph completo (corregido para preservar alpha en capas de lluvia y niebla):
# [0] Bosque base
# [1] Lluvia ligera
# [2] Lluvia media
# [3] Lluvia intensa
# [4] Niebla
# Combinar todo + agregar texto

filter_complex = (
    f"[0:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,format=rgba,gblur=sigma=1[forest];"
    
    # Lluvia ligera (rápida, más transparente)
    f"[1:v]fps=30,format=rgba,colorchannelmixer=aa=0.30,gblur=sigma=0.3[rain_light];"
    
    # Lluvia media (movimiento, más natural)
    f"[2:v]fps=25,format=rgba,colorchannelmixer=aa=0.22,gblur=sigma=0.6[rain_medium];"
    
    # Lluvia intensa (lenta, sutil y transparente)
    f"[3:v]fps=20,format=rgba,colorchannelmixer=aa=0.15,gblur=sigma=1.0[rain_heavy];"
    
    # Combinar capas de lluvia (screen/overlay mantienen luminancia sin tapar el fondo)
    f"[rain_light][rain_medium]blend=all_mode=screen[rain_blend1];"
    f"[rain_blend1][rain_heavy]blend=all_mode=overlay[rain_final];"
    
    # Agregar lluvia al bosque usando overlay que respeta alpha
    f"[forest][rain_final]overlay=shortest=1:format=auto[with_rain];"
    
    # Crear capa de 'sway' (suave movimiento horizontal/vertical para simular árboles moviéndose)
    f"[0:v]format=rgba,gblur=sigma=2,colorchannelmixer=aa=0.06[sway];"
    f"[with_rain][sway]overlay=x='sin(2*PI*t/12)*6':y='sin(2*PI*t/18)*3':shortest=1:format=auto[with_sway];"
    
    # Agregar niebla semitransparente (blanca difusa)
    f"[4:v]fps=15,noise=alls=10:allf=t,format=rgba,colorchannelmixer=aa=0.07,gblur=sigma=6[mist];"
    f"[with_sway][mist]overlay=shortest=1:format=auto[with_mist];"
    
    # Agregar mensajes de texto y convertir a yuv420p
    f"[with_mist]{text_filter_chain},format=yuv420p[final]"
)

print("Filtergraph construido")
print()

# ===== 3. CONSTRUIR COMANDO FFMPEG =====

print("3. Preparando renderizado...")

# Asegurar que existan los bucles de lluvia (light/medium/heavy)
RAIN_LIGHT = Path("assets/video/rain_light.mp4")
RAIN_MEDIUM = Path("assets/video/rain_medium.mp4")
RAIN_HEAVY = Path("assets/video/rain_heavy.mp4")
if not (RAIN_LIGHT.exists() and RAIN_MEDIUM.exists() and RAIN_HEAVY.exists()):
    print("  No existen bucles de lluvia — generando activos...")
    subprocess.run([".\\venv\\Scripts\\python.exe", "generate_rain_assets.py" ], check=True)

# Optional ambient rain sound (try to download a royalty-free loop if missing)
RAIN_SOUND = Path("assets/audio/rain_loop.mp3")
if not RAIN_SOUND.exists():
    try:
        import requests
        rain_candidates = [
            # Short royalty-free candidates (fallbacks)
            "https://cdn.pixabay.com/download/audio/2021/08/04/audio_f3bf3b.mp3",
            "https://files.freemusicarchive.org/storage-freemusicarchive-org/music/noise/Rain_loop.mp3"
        ]
        downloaded = False
        for url in rain_candidates:
            try:
                resp = requests.get(url, timeout=20)
                if resp.status_code == 200 and len(resp.content) > 1000:
                    RAIN_SOUND.parent.mkdir(parents=True, exist_ok=True)
                    with open(RAIN_SOUND, 'wb') as f:
                        f.write(resp.content)
                    print(f"  Rain sound downloaded: {RAIN_SOUND.name}")
                    downloaded = True
                    break
            except Exception:
                continue
        if not downloaded:
            print("  No rain loop found automatically; continuing without ambient rain audio")
    except Exception:
        print("  requests unavailable, skipping rain download (no rain audio)")

# Build ffmpeg inputs dynamically (rain layers only — particles disabled)
# (Particles were removed per request)
# We keep the generator script for future use but do not call it here.
if AUDIO_FILE and AUDIO_FILE.exists():
    # Con música (build inputs stepwise)
    cmd = [FFMPEG, "-nostdin", "-loop", "1", "-i", str(FOREST)]
    cmd += ["-stream_loop", "-1", "-i", str(RAIN_LIGHT),  # lluvia ligera
            "-stream_loop", "-1", "-i", str(RAIN_MEDIUM),  # lluvia media
            "-stream_loop", "-1", "-i", str(RAIN_HEAVY),  # lluvia intensa
            "-f", "lavfi", "-i", "color=0xffffff:s=1280x720:d=" + str(DURATION)]  # niebla

    # Optional ambient rain sound
    if RAIN_SOUND.exists():
        cmd += ["-stream_loop", "-1", "-i", str(RAIN_SOUND)]  # ambient rain sound

    # Music input
    cmd += ["-i", str(AUDIO_FILE)]  # música

    # determine indices for audio inputs and build audio mixing filter if needed
    def _input_idx(path):
        # returns the ffmpeg input index for the given path found in the cmd list
        pos = cmd.index(str(path))
        return sum(1 for i in range(pos) if cmd[i] == '-i') - 1

    audio_filter_ext = ""
    if RAIN_SOUND.exists():
        music_idx = _input_idx(AUDIO_FILE)
        rain_idx = _input_idx(RAIN_SOUND)
        audio_filter_ext = (
            f"[{music_idx}:a]volume=0.92[music];"
            f"[{rain_idx}:a]volume=0.20[rain];"
            f"[music][rain]amix=inputs=2:weights=1 0.25:dropout_transition=2[aout]"
        )
        audio_map_arg = "[aout]"
    else:
        music_idx = _input_idx(AUDIO_FILE)
        audio_map_arg = f"{music_idx}:a"

    # assemble filter_complex and map args
    filter_complex_full = filter_complex + (";" + audio_filter_ext if audio_filter_ext else "")
    cmd += ["-filter_complex", filter_complex_full, "-map", "[final]", "-map", audio_map_arg,
            "-c:v", "mpeg4", "-q:v", "5",
            "-c:a", "aac", "-ar", "44100", "-b:a", "192k",
            "-t", str(DURATION), "-r", "30", "-y", str(OUTPUT)]
else:
    # No music: use pink noise or ambient rain sound if available
    cmd = [FFMPEG, "-nostdin", "-loop", "1", "-i", str(FOREST)]
    cmd += ["-stream_loop", "-1", "-i", str(RAIN_LIGHT),
            "-stream_loop", "-1", "-i", str(RAIN_MEDIUM),
            "-stream_loop", "-1", "-i", str(RAIN_HEAVY),
            "-f", "lavfi", "-i", "color=0xffffff:s=1280x720:d=" + str(DURATION)]  # particles removed intentionally

    if RAIN_SOUND.exists():
        cmd += ["-stream_loop", "-1", "-i", str(RAIN_SOUND)]
        # pink noise input comes after rain sound so its index shifts
        cmd += ["-f", "lavfi", "-i", "anoisesrc=r=44100:c=2:d=" + str(DURATION)]
        # compute indices
        def _input_idx(path):
            pos = cmd.index(str(path))
            return sum(1 for i in range(pos) if cmd[i] == '-i') - 1
        rain_idx = _input_idx(RAIN_SOUND)
        noise_idx = _input_idx("anoisesrc=r=44100:c=2:d=" + str(DURATION))
        audio_filter_ext = (
            f"[{rain_idx}:a]volume=0.30[rain];"
            f"[{noise_idx}:a]volume=0.80[noise];"
            f"[noise][rain]amix=inputs=2:weights=1 0.6:dropout_transition=2[aout]"
        )
        filter_complex_full = filter_complex + ";" + audio_filter_ext
        audio_map_arg = "[aout]"
    else:
        # only noise
        cmd += ["-f", "lavfi", "-i", "anoisesrc=r=44100:c=2:d=" + str(DURATION)]
        # noise input is last; compute its input index
        def _input_idx_simple():
            return sum(1 for i in range(len(cmd)) if cmd[i] == '-i') - 1
        noise_idx = _input_idx_simple()
        audio_map_arg = f"{noise_idx}:a"
        filter_complex_full = filter_complex

    cmd += ["-filter_complex", filter_complex_full, "-map", "[final]", "-map", audio_map_arg,
            "-c:v", "mpeg4", "-q:v", "5",
            "-c:a", "aac", "-ar", "44100", "-b:a", "192k",
            "-t", str(DURATION), "-r", "30", "-y", str(OUTPUT)]

print()
print("4. Ejecutando FFmpeg...")
print("=" * 70)

try:
    result = subprocess.run(cmd, capture_output=False, timeout=300)
    
    if result.returncode == 0 and OUTPUT.exists():
        size_mb = OUTPUT.stat().st_size / 1024 / 1024
        print()
        print("=" * 70)
        print("VIDEO FINAL GENERADO")
        print("=" * 70)
        print(f"Archivo: {OUTPUT.name}")
        print(f"Tamaño: {size_mb:.1f} MB")
        print(f"Duración: {DURATION} segundos")
        print(f"Resolución: 1280x720@30fps")
        print()
        print("Características incluidas:")
        print("  ✓ Bosque brumoso de alta calidad")
        print("  ✓ Lluvia multicapa (3 intensidades)")
        print("  ✓ Niebla flotante animada")
        print("  ✓ Música ambiental royalty-free")
        print("  ✓ Mensajes motivadores cada 10s")
        print("  ✓ Audio de calidad 192kbps")
        print()
    else:
        print("Error: FFmpeg falló")
        exit(1)

except subprocess.TimeoutExpired:
    print("Error: Timeout (tardó demasiado)")
    exit(1)
except Exception as e:
    print(f"Error: {e}")
    exit(1)
