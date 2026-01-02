param()

$ErrorActionPreference = "Stop"

$ffmpegBin = "C:\Users\Admin\AppData\Local\Microsoft\WinGet\Packages\BtbN.FFmpeg.LGPL.Shared.8.0_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-n8.0.1-17-g27a297f186-win64-lgpl-shared-8.0\bin\ffmpeg.exe"
if (-not (Test-Path $ffmpegBin)) {
    throw "FFmpeg not found"
}

$outDir = Join-Path $PWD "out"
New-Item -ItemType Directory -Path $outDir -Force | Out-Null

$outputFile = Join-Path $outDir "bosque_lluvioso_60s.mp4"
$duration = 60
$width = 1280
$height = 720

Write-Host "Generating 60-second relaxing forest rain video..."
Write-Host ""

$filterComplex = "[0:v]format=rgba,colorchannelmixer=rr=0.2:gg=0.4:bb=0.35,gblur=sigma=6,split=3[base1][base2][base3];[base1][1:v]overlay=x=100:y=80:enable='between(t,0,60)'[with_rain];[base2]drawbox=x=60:y=40:w=1160:h=640:t=30:color=0x3d5252@0.8[window_frame];[base3]drawbox=x=0:y=600:w=300:h=120:t=fill:color=0xb8956a@0.9[coffee_area];[with_rain][window_frame]overlay=x=0:y=0[with_frame];[with_frame][coffee_area]overlay=x=0:y=0[almost_final];[2:v]drawcircle=r=20:c=white@0.6,blur=sigma=3,scale=60:60:force_original_aspect_ratio=decrease[steam];[almost_final][steam]overlay=x=90:y=550:enable='between(t,0,60)'[final];[final]drawbox=x=75:y=610:w=150:h=80:t=fill:color=0x8b6f47@0.95,drawbox=x=80:y=615:w=140:h=70:t=fill:color=0xd4a574@0.85[video_out]"

$cmdArgs = @(
    '-y',
    '-f', 'lavfi', '-i', "color=c=0x2d5a4f:s=${width}x${height}:d=${duration}:r=30",
    '-f', 'lavfi', '-i', "nullsrc=s=${width}x${height}:d=${duration}:r=30,format=rgba,drawtext=text='':start_number=0[nullout];[nullout]perlin=scale=50:seed=random:octaves=3:frequency=0.03[trees];color=c=0x1a3a2a:s=${width}x${height}:d=${duration}:r=30,format=rgba[bg];[trees]scale=${width}:${height}[scaled_trees]",
    '-f', 'lavfi', '-i', "sine=f=0.5:a=0.3:d=${duration}",
    '-f', 'lavfi', '-i', "anoisesrc=d=${duration}:r=44100:a=0.35:color=pink",
    '-filter_complex', $filterComplex,
    '-map', '[video_out]', '-map', '3:a',
    '-c:v', 'mpeg4', '-q:v', '2', '-pix_fmt', 'yuv420p',
    '-c:a', 'aac', '-b:a', '256k', '-ac', '2',
    '-t', '60',
    $outputFile
)

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
} else {
    Write-Host "Error generando video"
}
