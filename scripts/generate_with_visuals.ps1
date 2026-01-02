param()

$ErrorActionPreference = "Stop"

$ffmpegBin = "C:\Users\Admin\AppData\Local\Microsoft\WinGet\Packages\BtbN.FFmpeg.LGPL.Shared.8.0_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-n8.0.1-17-g27a297f186-win64-lgpl-shared-8.0\bin\ffmpeg.exe"
if (-not (Test-Path $ffmpegBin)) {
    throw "FFmpeg not found"
}

$outDir = Join-Path $PWD "out"
New-Item -ItemType Directory -Path $outDir -Force | Out-Null

$outputFile = Join-Path $outDir "bosque_ventana_cafe_60s.mp4"
$duration = 60
$width = 1280
$height = 720

Write-Host "Generando video: Bosque desde ventana con cafe animado..."
Write-Host ""

# Filtro completo: fondo bosque + lluvia + ventana + marco + cafe con animacion
$filterComplex = @"
[0:v]scale=${width}:${height},format=rgba,
colorchannelmixer=rr=0.35:gg=0.55:bb=0.5,
gblur=sigma=5,
geq=r='clip(r(X\,Y)-2*sin(t)*50,0,255)':g='clip(g(X\,Y)+1*cos(t)*30,0,255)':b='clip(b(X\,Y),0,255)',
drawbox=x=60:y=40:w=1160:h=640:t=25:color=0x3d5252@0.85,
drawbox=x=80:y=60:w=1120:h=600:t=8:color=0x2d4a42@0.6,
drawbox=x=640:y=40:w=3:h=640:t=fill:color=0x1a2d28@0.8,
drawbox=x=60:y=360:w=1160:h=3:t=fill:color=0x1a2d28@0.8
[framed];

[1:v]scale=${width}:${height},format=rgba,
noise=alls=50:allf=t+u,
gblur=sigma=1.5,
colorchannelmixer=aa=0.4,
format=rgba
[rain];

[2:v]scale=${width}:${height},format=rgba,
drawbox=x=0:y=600:w=300:h=120:t=fill:color=0xb8956a@0.9,
drawbox=x=10:y=610:w=140:h=100:t=fill:color=0x8b6f47@0.95,
drawbox=x=15:y=615:w=130:h=90:t=fill:color=0xd4a574@0.85,
drawtext=text='':fontsize=20:x=40:y=625,
drawcircle=r='8+3*sin(t*2)':c=white@0.5:t=fill:x=80:y=590:enable='between(t,0,60)'
[coffee_cup];

[framed][rain]blend=screen:all_opacity=0.45[with_rain];
[with_rain][coffee_cup]overlay=x=0:y=0[final]
"@

$cmdArgs = @(
    '-y',
    '-f', 'lavfi', '-i', "color=c=0x1a4d42:s=${width}x${height}:d=${duration}:r=30",
    '-f', 'lavfi', '-i', "color=c=0x000000:s=${width}x${height}:d=${duration}:r=30",
    '-f', 'lavfi', '-i', "color=c=0x000000:s=${width}x${height}:d=${duration}:r=30",
    '-f', 'lavfi', '-i', "anoisesrc=d=${duration}:r=44100:a=0.35:color=pink",
    '-filter_complex', $filterComplex,
    '-map', '[final]', '-map', '3:a',
    '-c:v', 'mpeg4', '-q:v', '1', '-pix_fmt', 'yuv420p',
    '-c:a', 'aac', '-b:a', '256k', '-ac', '2',
    '-t', '60',
    $outputFile
)

Write-Host "Procesando con FFmpeg..."
Write-Host ""
& $ffmpegBin @cmdArgs

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=========================================="
    Write-Host "VIDEO LISTO"
    Write-Host "=========================================="
    Write-Host ""
    Write-Host "Archivo: $outputFile"
    Write-Host "Duracion: 60 segundos"
    Write-Host "Resolucion: 1280x720"
    Write-Host "Calidad: MPEG4 AAC"
    Write-Host ""
    Write-Host "Elementos:"
    Write-Host "- Bosque con efecto de movimiento"
    Write-Host "- Ventana con marco doble"
    Write-Host "- Lluvia animada"
    Write-Host "- Taza de cafe con vapor"
    Write-Host ""
} else {
    Write-Host "Error"
}
