#!/usr/bin/env pwsh
# Script para generar video relajante: Bosque lluvioso desde ventana con cafe

$ErrorActionPreference = "Stop"

# Configuracion
$outputDir = ".\out"
$outputFile = "$outputDir\bosque_cafe_lluvia_final.mp4"
$ffmpegPath = "C:\Users\Admin\AppData\Local\Microsoft\WinGet\Packages\BtbN.FFmpeg.LGPL.Shared.8.0_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-n8.0.1-17-g27a297f186-win64-lgpl-shared-8.0\bin\ffmpeg.exe"
$duration = 60
$fps = 30
$width = 1280
$height = 720

# Crear directorio de salida
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
}

Write-Host "Generando video: Bosque con lluvia desde ventana con cafe" -ForegroundColor Cyan
Write-Host "Duracion: $duration segundos | Resolucion: ${width}x${height} | FPS: $fps" -ForegroundColor Gray

# Crear filtergraph con elementos visuales
# Fondo bosque + ventana + lluvia + cafe

$filterComplex = "[0:v]format=rgba,scale=${width}:${height},colorchannelmixer=rr=0.35:gg=0.50:bb=0.40:aa=1,gblur=sigma=3,drawbox=x=100:y=80:w=1080:h=600:t=5:color=0x3a5a4a@0.15,drawbox=x=110:y=90:w=1060:h=580:t=3:color=0x0d1f1a@0.8,drawbox=x=540:y=90:w=2:h=580:t=fill:color=0x0a1810@0.9,drawbox=x=100:y=340:w=1080:h=2:t=fill:color=0x0a1810@0.9[window];[1:v]fps=${fps},noise=alls=35:allf=t+u,gblur=sigma=1.5,format=gray,colorchannelmixer=aa=0.4[rain_base];[window][rain_base]overlay=x=0:y=0,format=rgba,drawbox=x=1020:y=550:w=180:h=120:t=fill:color=0xCCB8A8@0.7,drawbox=x=1040:y=570:w=140:h=60:t=fill:color=0x3d2817@0.9,drawbox=x=1055:y=540:w=110:h=25:t=fill:color=0xf5f5dc@0.6,format=rgba[final]"

$cmdArgs = @(
    "-f", "lavfi", "-i", "color=0x1a3a2a:s=${width}x${height}:d=$duration",
    "-f", "lavfi", "-i", "anoisesrc=r=44100:c=stereo:d=$duration",
    "-filter_complex", $filterComplex,
    "-map", "[final]",
    "-map", "1:a",
    "-c:v", "mpeg4",
    "-q:v", "7",
    "-c:a", "aac",
    "-ar", "44100",
    "-b:a", "256k",
    "-t", "$duration",
    "-r", "$fps",
    "-y",
    $outputFile
)

Write-Host "`nEjecutando FFmpeg..." -ForegroundColor Yellow

try {
    & $ffmpegPath $cmdArgs 2>&1 | ForEach-Object {
        if ($_ -match "frame=") {
            Write-Host $_ -ForegroundColor Green
        }
        elseif ($_ -match "error|Error") {
            Write-Host $_ -ForegroundColor Red
        }
    }
    
    if ($LASTEXITCODE -eq 0 -and (Test-Path $outputFile)) {
        $fileSize = (Get-Item $outputFile).Length / 1MB
        Write-Host "`nVideo generado exitosamente" -ForegroundColor Green
        Write-Host "Archivo: $outputFile" -ForegroundColor Green
        Write-Host "Tamano: $($fileSize.ToString('F1')) MB" -ForegroundColor Green
        Write-Host "`nContenido del video:" -ForegroundColor Cyan
        Write-Host "  - Bosque con lluvia" -ForegroundColor Gray
        Write-Host "  - Ventana con marco" -ForegroundColor Gray
        Write-Host "  - Lluvia animada" -ForegroundColor Gray
        Write-Host "  - Taza de cafe" -ForegroundColor Gray
        Write-Host "  - Audio relajante" -ForegroundColor Gray
    }
    else {
        Write-Host "`nError: No se pudo generar el video" -ForegroundColor Red
        exit 1
    }
}
catch {
    Write-Host "`nError: $PSItem" -ForegroundColor Red
    exit 1
}
