@echo off
setlocal enabledelayedexpansion

REM Ruta de FFmpeg
set FFMPEG=C:\Users\Admin\AppData\Local\Microsoft\WinGet\Packages\BtbN.FFmpeg.LGPL.Shared.8.0_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-n8.0.1-17-g27a297f186-win64-lgpl-shared-8.0\bin\ffmpeg.exe

REM Extraer frame a los 15 segundos
echo Extrayendo preview frame...
!FFMPEG! -i out\bosque_completo_final.mp4 -ss 00:00:15 -vframes 1 -c:v mjpeg out\preview_frame.jpg -y

if exist out\preview_frame.jpg (
    echo OK: Frame extraido exitosamente
    dir out\preview_frame.jpg
) else (
    echo ERROR: No se pudo crear el frame
    exit /b 1
)
