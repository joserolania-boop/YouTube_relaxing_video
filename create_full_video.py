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
        "https://cdn.pixabay.com/download/audio/2020/07/09/audio_37b6f0.mp3",  # alternate calm (Pixabay)
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

    # Fallback: prefer already-generated or processed ambient tracks if present
    alt_processed = Path("assets/audio/ambient_music_processed.mp3")
    alt_generated = Path("assets/audio/ambient_music_generated.mp3")
    if (AUDIO_FILE is None) or (not AUDIO_FILE.exists()):
        if alt_processed.exists():
            print(f"  Usando pista procesada: {alt_processed.name}")
            AUDIO_FILE = alt_processed
        elif alt_generated.exists():
            print(f"  Usando pista sintetizada: {alt_generated.name}")
            AUDIO_FILE = alt_generated
        else:
            # Scan user-provided audio files and pick the best by loudness (closest to target)
            print("  Buscando pistas en assets/audio para elegir la mejor melodía...")
            candidates = []
            for ext in ('*.mp3', '*.wav', '*.m4a', '*.aac'):
                candidates.extend(sorted(Path('assets/audio').glob(ext)))
            best = None
            best_score = 1e9
            target = -6.0  # preferred mean volume
            for c in candidates:
                # skip the fallback/noise files
                if c.name.startswith('ambient_music') or c.name.startswith('diagnostic'):
                    continue
                try:
                    p = subprocess.run([FFMPEG, '-i', str(c), '-af', 'volumedetect', '-f', 'null', '-'], capture_output=True, text=True, timeout=20)
                    stderr = p.stderr or ''
                    mv = None
                    for line in stderr.splitlines():
                        if 'mean_volume' in line:
                            try:
                                mv = float(line.split(':')[-1].strip().split()[0])
                            except Exception:
                                mv = None
                            break
                    if mv is None:
                        continue
                    # ignore extremely quiet files (likely silence or very low gain)
                    if mv < -35:
                        continue
                    score = abs(mv - target)
                    if score < best_score:
                        best_score = score
                        best = (c, mv)
                except Exception:
                    continue
            if best:
                AUDIO_FILE = best[0]
                print(f"  Seleccionada: {AUDIO_FILE.name} (mean={best[1]:.1f} dB)")
            else:
                print("  No se encontró pista adecuada; se usará el fallback (ruido coloreado)")

    # Prefer explicit user-added relaxing melodies (relax/meditation/flute/piano) over generic ambient_music
    user_patterns = ('*relax*', '*meditat*', '*flute*', '*piano*', '*calm*', '*please*')
    user_candidates = []
    for pat in user_patterns:
        user_candidates.extend(sorted(Path('assets/audio').glob(pat)))
    if user_candidates:
        print('  Se detectaron melodías nuevas en assets/audio, evaluando para elegir la mejor...')
        best = None
        best_score = 1e9
        target = -6.0
        for c in user_candidates:
            try:
                p = subprocess.run([FFMPEG, '-i', str(c), '-af', 'volumedetect', '-f', 'null', '-'], capture_output=True, text=True, timeout=20)
                stderr = p.stderr or ''
                mv = None
                for line in stderr.splitlines():
                    if 'mean_volume' in line:
                        try:
                            mv = float(line.split(':')[-1].strip().split()[0])
                        except Exception:
                            mv = None
                        break
                if mv is None or mv < -35:
                    continue
                score = abs(mv - target)
                if score < best_score:
                    best_score = score
                    best = (c, mv)
            except Exception:
                continue
        if best:
            AUDIO_FILE = best[0]
            print(f"  Elegida pista de usuario: {AUDIO_FILE.name} (mean={best[1]:.1f} dB)")
        else:
            print('  Ninguna de las melodías nuevas resultó adecuada; manteniendo la pista actual')

print()

# ===== 2. CONSTRUIR FILTERGRAPH =====
print("2. Construyendo filtergraph con lluvia multicapa + mensajes...")
print()

# Mensajes / citas famosas sobre la vida (aparecen cada bloque con caja y sombra para integrarse en la escena)
messages = [
    ("Ser o no ser; esa es la cuestión. — W. Shakespeare", 2, 6),
    ("Lo que buscas te está buscando a ti. — Rumi", 8, 12),
    ("Un viaje de mil millas comienza con un solo paso. — Lao Tzu", 14, 18),
    ("Si quieres ser feliz, sé. — L. Tolstói", 20, 24),
    ("La felicidad de tu vida depende de la calidad de tus pensamientos. — Marco Aurelio", 26, 30),
]

# Generar filtros de texto (drawtext) - integrado en el bosque: serif, caja suave y color natural
text_filter_chain = ""
for msg, start, end in messages:
    if text_filter_chain:
        text_filter_chain += ","
    # Responsive fontsize and natural color; slide-in from below (0.6s) for a gentle appearance
    # Note: escape commas in expressions (\,) so ffmpeg doesn't split options
    text_filter_chain += (
        f"drawtext=fontsize='if(gte(w,1280),34,22)':fontcolor=0xDCEEE0@0.95:box=1:boxcolor=black@0.30:boxborderw=6:"
        f"shadowcolor=0x062814@0.7:shadowx=2:shadowy=2:fontfile=/Windows/Fonts/Georgia.ttf:text='{msg}':"
        f"x=(w-text_w)/2:y=h-120+40*(1-min(1\,max(0\,((t-{start})/0.6)))):enable='between(t,{start},{end})'"
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
    # Motion-blur temporal en la lluvia para streaks más naturales
    f"[rain_final]tblend=all_mode=average:all_opacity=0.65[rain_tb];"
    
    # Agregar lluvia al bosque usando la versión con motion-blur
    f"[forest][rain_tb]overlay=shortest=1:format=auto[with_rain];"
    
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
    music_idx = _input_idx(AUDIO_FILE)
    # Ensure music is audible: apply a slight gain and gentle stereo motion
    if RAIN_SOUND.exists():
        rain_idx = _input_idx(RAIN_SOUND)
        # Music louder and normalized; increase and shape rain so it's audible but not overpowering
        audio_filter_ext = (
            f"[{music_idx}:a]loudnorm=I=-8:TP=-1.0:LRA=7,volume=1.0[music_p];"
            f"[{rain_idx}:a]highpass=f=150,lowpass=f=3500,volume=0.18[rain];"
            f"[music_p][rain]amix=inputs=2:weights=1 0.18:dropout_transition=2[aout];"
            f"[aout]dynaudnorm=f=150:g=12[aout2]"
        )
        audio_map_arg = "[aout2]"
    else:
        # No rain audio file available: create a synthetic rain-like ambient audio using lavfi
        noise_lavfi = f"anoisesrc=color=brown:amplitude=0.5:d={DURATION}"
        cmd += ["-f", "lavfi", "-i", noise_lavfi]
        noise_idx = _input_idx(noise_lavfi)
        # Apply shaping so synthetic noise sounds like rain and is more audible in the mix
        audio_filter_ext = (
            f"[{music_idx}:a]loudnorm=I=-8:TP=-1.0:LRA=7,volume=1.0[music_p];"
            f"[{noise_idx}:a]highpass=f=200,lowpass=f=4000,volume=0.15,aecho=0.5:0.25:200:0.2[rain];"
            f"[music_p][rain]amix=inputs=2:weights=1 0.15:dropout_transition=1[aout];"
            f"[aout]dynaudnorm=f=150:g=12[aout2]"
        )
        audio_map_arg = "[aout2]"

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
        # Add a gentle colored noise (brown) to fill gaps and add texture — shaped to sound like rain
        noise_lavfi = f"anoisesrc=color=brown:amplitude=0.35:d={DURATION}"
        cmd += ["-f", "lavfi", "-i", noise_lavfi]
        # compute indices
        def _input_idx(path):
            pos = cmd.index(str(path))
            return sum(1 for i in range(pos) if cmd[i] == '-i') - 1
        rain_idx = _input_idx(RAIN_SOUND)
        noise_idx = _input_idx(noise_lavfi)
        audio_filter_ext = (
            f"[{rain_idx}:a]lowpass=f=2500,volume=0.60[rain];"
            f"[{noise_idx}:a]highpass=f=200,lowpass=f=4000,volume=0.25[noise];"
            f"[noise][rain]amix=inputs=2:weights=0.6 1:dropout_transition=2[aout];"
            f"[aout]dynaudnorm=f=150:g=12[aout2]"
        )
        filter_complex_full = filter_complex + ";" + audio_filter_ext
        audio_map_arg = "[aout2]"
    else:
        # only noise: generate brown noise and shape it to resemble rain (less harsh than white noise)
        noise_lavfi = f"anoisesrc=color=brown:amplitude=0.35:d={DURATION}"
        cmd += ["-f", "lavfi", "-i", noise_lavfi]
        # noise input is last; compute its input index
        def _input_idx_simple():
            return sum(1 for i in range(len(cmd)) if cmd[i] == '-i') - 1
        noise_idx = _input_idx_simple()
        audio_filter_ext = (
            f"[{noise_idx}:a]highpass=f=200,lowpass=f=4000,volume=0.45[rain];"
            f"[rain]dynaudnorm=f=150:g=12[aout]"
        )
        filter_complex_full = filter_complex + ";" + audio_filter_ext
        audio_map_arg = "[aout]"

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
