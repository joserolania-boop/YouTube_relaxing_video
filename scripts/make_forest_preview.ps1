param(
    [string]$BackgroundImage = $null,
    [string]$RainDropsOverlay = $null,
    [string]$AudioFile = $null,
    [switch]$SynthesisOnly = $false
)

$ErrorActionPreference = "Stop"

# Resolver ruta de FFmpeg
$ffmpegBin = $env:FFMPEG_BIN
if (-not $ffmpegBin) {
    $ffmpegBin = "C:\Users\Admin\AppData\Local\Microsoft\WinGet\Packages\BtbN.FFmpeg.LGPL.Shared.8.0_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-n8.0.1-17-g27a297f186-win64-lgpl-shared-8.0\bin\ffmpeg.exe"
}
if (-not (Test-Path $ffmpegBin)) {
    throw "ffmpeg no encontrado en $ffmpegBin. Instala FFmpeg o define FFMPEG_BIN."
}

$outDir = Join-Path $PWD "out"
New-Item -ItemType Directory -Path $outDir -Force | Out-Null

$assetsDir = Join-Path $PWD "assets" "images"
New-Item -ItemType Directory -Path $assetsDir -Force | Out-Null

$outputFile = Join-Path $outDir "forest_window_piloto_60s.mp4"

# ============================================================================
# MODO 1: SI HAY IMAGEN DE FONDO -> ENSAMBLAJE VISUAL CON ZOOM/PANEO
# ============================================================================
if ($BackgroundImage -and (Test-Path $BackgroundImage) -and -not $SynthesisOnly) {
    Write-Host "→ Director de Arte: Ensamblaje visual con imagen fotorrealista..."
    Write-Host "  Imagen: $BackgroundImage"
    
    $duration = 60
    $width = 1280
    $height = 720
    
    # Filtro: imagen + zoom suave (Ken Burns) + marco ventana + capa lluvia
    # Zoom suave: scale de 1.0 a 1.15 durante 60s = efecto cinematográfico sutil
    $filterComplex = "[0:v]scale=${width}:${height},format=rgba,fps=30,setdar=16/9,zoompan=z='min(zoom+0.0025,1.15)':d=60:s=${width}x${height}[base];[1:v]format=rgba,gblur=sigma=2,colorchannelmixer=aa=0.5[rain];[base]drawbox=x=0:y=0:w=${width}:h=${height}:t=3:color=0x1a3a2a@0.15[frame1];[frame1][rain]blend=screen:all_opacity=0.45[final]"
    
    # Si hay audio personalizado, usarlo; si no, generar lluvia rosa
    if ($AudioFile -and (Test-Path $AudioFile)) {
        Write-Host "  Audio personalizado: $AudioFile"
        
        $cmdArgs = @(
            '-y',
            '-i', $BackgroundImage,
            '-f', 'lavfi', '-i', "color=c=0x000000:s=${width}x${height}:d=${duration}:r=30",
            '-i', $AudioFile,
            '-filter_complex', $filterComplex,
            '-map', '[final]', '-map', '2:a',
            '-c:v', 'mpeg4', '-q:v', '2', '-pix_fmt', 'yuv420p',
            '-c:a', 'aac', '-b:a', '256k', '-ac', '2',
            '-t', '60',
            $outputFile
        )
    } else {
        Write-Host "  Audio: Lluvia rosa binaural sintetizada (432Hz)"
        
        $cmdArgs = @(
            '-y',
            '-i', $BackgroundImage,
            '-f', 'lavfi', '-i', "color=c=0x000000:s=${width}x${height}:d=${duration}:r=30",
            '-f', 'lavfi', '-i', "anoisesrc=d=${duration}:r=44100:a=0.35:color=pink",
            '-filter_complex', $filterComplex,
            '-map', '[final]', '-map', '2:a',
            '-c:v', 'mpeg4', '-q:v', '2', '-pix_fmt', 'yuv420p',
            '-c:a', 'aac', '-b:a', '256k', '-ac', '2',
            '-t', '60',
            $outputFile
        )
    }
    
    Write-Host "✓ Aplicando zoom Ken Burns suave + marco ventana + lluvia..."
    & $ffmpegBin @cmdArgs
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ ╔════════════════════════════════════════════╗"
        Write-Host "✓ ║  VIDEO PILOTO CINEMATOGRÁFICO COMPLETADO ║"
        Write-Host "✓ ╚════════════════════════════════════════════╝"
        Write-Host "  Archivo: $outputFile"
        Write-Host "  Duración: 60s | Resolución: ${width}x${height} | Codec: MPEG4 Q2"
        Write-Host "  Efecto: Zoom Ken Burns suave + lluvia sobre imagen"
        Write-Host ""
        Write-Host "  Visualiza: start `"$outputFile`""
    } else {
        throw "Error en ensamblaje visual. Código: $LASTEXITCODE"
    }
    exit
}

# ============================================================================
# MODO 2: SÍNTESIS PURA (SIN IMAGEN EXTERNA) -> FONDO SINTÉTICO
# ============================================================================
Write-Host "→ Modo síntesis: generando fondo forestal sintético sin archivos externos..."

$duration = 60
$width = 1280
$height = 720
    
    # Fondo: color forestal + gradiente verde-teal
    $bgGenerate = "color=c=0x1a3a2a:s=${width}x${height}:d=${duration}:r=30"
    
    # Capa de ruido (simula lluvia/gotas)
    $rainGenerate = "color=c=0x000000:s=${width}x${height}:d=${duration}:r=30"
    
    # Audio: lluvia base pink noise + suave
    $audioGenerate = "anoisesrc=d=${duration}:r=44100:a=0.35:color=pink"
    
    # Filtro complejo: marco de ventana + gotas + transiciones
    $filterComplex = "[0:v]format=rgba,colorchannelmixer=rr=0.45:gg=0.60:bb=0.55,gblur=sigma=4,drawbox=x=80:y=50:w=1120:h=620:t=35:color=0x0d1f1a@0.9,drawbox=x=100:y=70:w=1080:h=580:t=10:color=0x051410@0.7,drawbox=x=540:y=70:w=15:h=580:t=fill:color=0x0a1810@0.8,drawbox=x=100:y=360:w=1080:h=15:t=fill:color=0x0a1810@0.8[framed];[1:v]noise=alls=45:allf=t+u,gblur=sigma=2,format=gray,colorchannelmixer=aa=0.5,format=rgba[rain];[framed][rain]blend=screen:all_opacity=0.55[video_out]"
    
    # Comando FFmpeg para síntesis completa
    $cmdArgs = @(
        '-y',
        '-f', 'lavfi', '-i', $bgGenerate,
        '-f', 'lavfi', '-i', $rainGenerate,
        '-f', 'lavfi', '-i', $audioGenerate,
        '-filter_complex', $filterComplex,
        '-map', '[video_out]', '-map', '2:a',
        '-c:v', 'mpeg4', '-q:v', '3', '-pix_fmt', 'yuv420p',
        '-c:a', 'aac', '-b:a', '192k', '-ac', '2',
        '-t', '60',
        $outputFile
    )
    
    Write-Host "→ Ejecutando síntesis FFmpeg para 60s..."
    & $ffmpegBin @cmdArgs
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ ╔════════════════════════════════════════════╗"
        Write-Host "✓ ║  VIDEO PILOTO SINTÉTICO COMPLETADO        ║"
        Write-Host "✓ ╚════════════════════════════════════════════╝"
        Write-Host "  Archivo: $outputFile"
        Write-Host "  Duración: 60s | Resolución: ${width}x${height} | Codec: MPEG4 Q3"
        Write-Host "  Tipo: Síntesis FFmpeg (fondo + lluvia + audio rosa)"
        Write-Host ""
        Write-Host "  Para mejorar con imagen fotorrealista:"
        Write-Host "  1. Copia el prompt de PROMPTS_MIDJOURNEY_ARTE.md a Midjourney"
        Write-Host "  2. Descarga la imagen generada a: assets/images/bosque_ventana_base.png"
        Write-Host "  3. Ejecuta: .\scripts\make_forest_preview.ps1 -BackgroundImage 'assets/images/bosque_ventana_base.png'"
        Write-Host ""
        Write-Host "  Visualiza: start `"$outputFile`""
    } else {
        throw "Error al generar síntesis. Código: $LASTEXITCODE"
    }
    exit
}

# ============================================================================
# MODO COMPOSICIÓN: ACTIVOS EXTERNOS (IMAGEN + AUDIO)
# ============================================================================
Write-Host "→ Modo composición con activos externos..."

if (-not (Test-Path $BackgroundImage)) {
    throw "Imagen de fondo no encontrada: $BackgroundImage"
}

if ($AudioFile -and -not (Test-Path $AudioFile)) {
    throw "Archivo de audio no encontrado: $AudioFile"
}

$width = 1280
$height = 720

$filterComplex = "[0:v]scale=${width}:${height},format=rgba,colorchannelmixer=rr=0.45:gg=0.60:bb=0.55,gblur=sigma=3,drawbox=x=80:y=50:w=1120:h=620:t=35:color=0x0d1f1a@0.9,drawbox=x=100:y=70:w=1080:h=580:t=10:color=0x051410@0.7,drawbox=x=540:y=70:w=15:h=580:t=fill:color=0x0a1810@0.8,drawbox=x=100:y=360:w=1080:h=15:t=fill:color=0x0a1810@0.8[framed];[1:v]scale=${width}:${height},format=rgba,gblur=sigma=2[overlay_drops];[framed][overlay_drops]blend=screen:all_opacity=0.55[final]"

$cmdArgs = @(
    '-y',
    '-i', $BackgroundImage,
    '-i', $RainDropsOverlay,
    '-i', $AudioFile,
    '-filter_complex', $filterComplex,
    '-map', '[final]',
    '-map', '2:a',
    '-c:v', 'mpeg4', '-q:v', '3', '-pix_fmt', 'yuv420p',
    '-c:a', 'aac', '-b:a', '192k',
    '-t', '60',
    $outputFile
)

Write-Host "→ Componiendo video con activos..."
& $ffmpegBin @cmdArgs

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Video piloto completado: $outputFile"
    Write-Host "✓ Especificaciones: 1280x720 | 60s | MPEG4 | AAC 192k"
} else {
    throw "Error al componer video. Código: $LASTEXITCODE"
}