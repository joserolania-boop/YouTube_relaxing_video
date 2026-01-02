param(
    [string]$BackgroundImage = $null,
    [string]$AudioFile = $null
)

$ErrorActionPreference = "Stop"

# Resolver ruta de FFmpeg
$ffmpegBin = $env:FFMPEG_BIN
if (-not $ffmpegBin) {
    $ffmpegBin = "C:\Users\Admin\AppData\Local\Microsoft\WinGet\Packages\BtbN.FFmpeg.LGPL.Shared.8.0_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-n8.0.1-17-g27a297f186-win64-lgpl-shared-8.0\bin\ffmpeg.exe"
}
if (-not (Test-Path $ffmpegBin)) {
    throw "❌ FFmpeg no encontrado. Instala FFmpeg o define FFMPEG_BIN."
}

$outDir = Join-Path $PWD "out"
New-Item -ItemType Directory -Path $outDir -Force | Out-Null

$assetsDir = Join-Path $PWD "assets" "images"
New-Item -ItemType Directory -Path $assetsDir -Force | Out-Null

$outputFile = Join-Path $outDir "forest_window_piloto_60s.mp4"

$duration = 60
$width = 1280
$height = 720

# ============================================================================
# MODO 1: CON IMAGEN FOTORREALISTA (Director de Arte Activado)
# ============================================================================
if ($BackgroundImage -and (Test-Path $BackgroundImage)) {
    Write-Host "✨ DIRECTOR DE ARTE: Ensamblaje visual cinematográfico"
    Write-Host "───────────────────────────────────────────────────"
    Write-Host "📸 Imagen base: $BackgroundImage"
    
    # Zoom Ken Burns suave: escala de 1.0 a 1.15 durante 60s
    # Marco ventana oscuro para enmarcar la composición
    # Capa de lluvia/gotas en blend screen para efecto transparente
    $filterComplex = "[0:v]scale=${width}:${height},format=rgba,fps=30,setdar=16/9,zoompan=z='min(zoom+0.0025,1.15)':d=60:s=${width}x${height}[zoomed];[1:v]format=rgba,gblur=sigma=2,colorchannelmixer=aa=0.5,format=rgba[rain];[zoomed]drawbox=x=0:y=0:w=${width}:h=${height}:t=4:color=0x1a2f2a@0.2[frame];[frame][rain]blend=screen:all_opacity=0.45[final]"
    
    # Generar audio si no se proporciona
    if (-not $AudioFile -or -not (Test-Path $AudioFile)) {
        Write-Host "🎵 Audio: Lluvia rosa binaural generada (44.1kHz, 432Hz root)"
        $audioInput = "anoisesrc=d=${duration}:r=44100:a=0.35:color=pink"
        $audioMap = "1:a"
    } else {
        Write-Host "🎵 Audio personalizado: $AudioFile"
        $audioInput = "-i `"$AudioFile`""
        $audioMap = "2:a"
    }
    
    Write-Host "⚙️  Aplicando: Zoom Ken Burns + Marco Ventana + Lluvia"
    Write-Host "⏱️  Duración: 60 segundos"
    Write-Host ""
    
    if (-not $AudioFile -or -not (Test-Path $AudioFile)) {
        $cmdArgs = @(
            '-y',
            '-i', $BackgroundImage,
            '-f', 'lavfi', '-i', "color=c=0x000000:s=${width}x${height}:d=${duration}:r=30",
            '-f', 'lavfi', '-i', $audioInput,
            '-filter_complex', $filterComplex,
            '-map', '[final]',
            '-map', '2:a',
            '-c:v', 'mpeg4', '-q:v', '2', '-pix_fmt', 'yuv420p',
            '-c:a', 'aac', '-b:a', '256k', '-ac', '2',
            '-t', '60',
            $outputFile
        )
    } else {
        $cmdArgs = @(
            '-y',
            '-i', $BackgroundImage,
            '-f', 'lavfi', '-i', "color=c=0x000000:s=${width}x${height}:d=${duration}:r=30",
            '-i', $AudioFile,
            '-filter_complex', $filterComplex,
            '-map', '[final]',
            '-map', '2:a',
            '-c:v', 'mpeg4', '-q:v', '2', '-pix_fmt', 'yuv420p',
            '-c:a', 'aac', '-b:a', '256k', '-ac', '2',
            '-t', '60',
            $outputFile
        )
    }
    
    & $ffmpegBin @cmdArgs
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "╔════════════════════════════════════════════════════════╗"
        Write-Host "║        ✓ VIDEO PILOTO CINEMATOGRÁFICO LISTO           ║"
        Write-Host "╚════════════════════════════════════════════════════════╝"
        Write-Host ""
        Write-Host "📄 Archivo: $outputFile"
        Write-Host "🎬 Duración: 60 segundos | Resolución: ${width}x${height}"
        Write-Host "🎥 Codec: MPEG4 (Q2 Alta Calidad) | Audio: AAC 256k estéreo"
        Write-Host "✨ Efectos: Zoom Ken Burns + Marco Ventana + Lluvia"
        Write-Host ""
        Write-Host "▶️  Para visualizar:"
        Write-Host "   start `"$outputFile`""
        Write-Host ""
    } else {
        throw "❌ Error en ensamblaje visual. Código: $LASTEXITCODE"
    }
    exit
}

# ============================================================================
# MODO 2: SÍNTESIS PURA (sin imagen externa)
# ============================================================================
Write-Host "🔧 MODO SÍNTESIS: Generando bosque forestal sintético"
Write-Host "──────────────────────────────────────────────────"
Write-Host "📐 Resolución: ${width}x${height} | Duración: 60s"

$filterComplex = "[0:v]format=rgba,colorchannelmixer=rr=0.45:gg=0.60:bb=0.55,gblur=sigma=4,drawbox=x=80:y=50:w=1120:h=620:t=35:color=0x0d1f1a@0.9,drawbox=x=100:y=70:w=1080:h=580:t=10:color=0x051410@0.7,drawbox=x=540:y=70:w=15:h=580:t=fill:color=0x0a1810@0.8,drawbox=x=100:y=360:w=1080:h=15:t=fill:color=0x0a1810@0.8[framed];[1:v]noise=alls=45:allf=t+u,gblur=sigma=2,format=gray,colorchannelmixer=aa=0.5,format=rgba[rain];[framed][rain]blend=screen:all_opacity=0.55[video_out]"

$cmdArgs = @(
    '-y',
    '-f', 'lavfi', '-i', "color=c=0x1a3a2a:s=${width}x${height}:d=${duration}:r=30",
    '-f', 'lavfi', '-i', "color=c=0x000000:s=${width}x${height}:d=${duration}:r=30",
    '-f', 'lavfi', '-i', "anoisesrc=d=${duration}:r=44100:a=0.35:color=pink",
    '-filter_complex', $filterComplex,
    '-map', '[video_out]', '-map', '2:a',
    '-c:v', 'mpeg4', '-q:v', '3', '-pix_fmt', 'yuv420p',
    '-c:a', 'aac', '-b:a', '192k', '-ac', '2',
    '-t', '60',
    $outputFile
)

Write-Host "⚙️  Síntesis en curso..."
Write-Host ""
& $ffmpegBin @cmdArgs

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "╔════════════════════════════════════════════════════════╗"
    Write-Host "║            ✓ VIDEO PILOTO LISTO (SÍNTESIS)           ║"
    Write-Host "╚════════════════════════════════════════════════════════╝"
    Write-Host ""
    Write-Host "📄 Archivo: $outputFile"
    Write-Host "🎬 Duración: 60s | Resolución: ${width}x${height}"
    Write-Host "🎥 Codec: MPEG4 (Q3) | Audio: AAC 192k mono"
    Write-Host "✨ Tipo: Síntesis FFmpeg (fondo + lluvia + audio rosa)"
    Write-Host ""
    Write-Host "📈 PARA MEJORAR CON IMAGEN FOTORREALISTA:"
    Write-Host ""
    Write-Host "1️⃣  Abre el archivo PROMPTS_MIDJOURNEY_ARTE.md"
    Write-Host "2️⃣  Copia el prompt principal a Midjourney y genera la imagen"
    Write-Host "3️⃣  Descarga la imagen a: assets/images/bosque_ventana_base.png"
    Write-Host "4️⃣  Ejecuta:"
    Write-Host "    .\scripts\make_forest_preview_v2.ps1 -BackgroundImage 'assets/images/bosque_ventana_base.png'"
    Write-Host ""
    Write-Host "▶️  Para visualizar ahora:"
    Write-Host "   start `"$outputFile`""
    Write-Host ""
} else {
    throw "❌ Error en síntesis. Código: $LASTEXITCODE"
}
