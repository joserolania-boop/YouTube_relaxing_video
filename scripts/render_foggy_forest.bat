@echo off
setlocal enabledelayedexpansion

REM GENERADOR: Bosque Brumoso - Estilo Referencia (xNN7iTA57jM)
REM Sin ventana, sin cafe. Solo: Bosque denso + niebla animada + audio ambiente

set "FFMPEG=C:\Users\Admin\AppData\Local\Microsoft\WinGet\Packages\BtbN.FFmpeg.LGPL.Shared.8.0_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-n8.0.1-17-g27a297f186-win64-lgpl-shared-8.0\bin\ffmpeg.exe"
set "OUTPUT=.\out\bosque_brumoso_60s.mp4"
set "DURATION=60"
set "FPS=30"
set "W=1280"
set "H=720"

if not exist ".\out" mkdir ".\out"

echo Generando: Bosque Brumoso (estilo xNN7iTA57jM)
echo Duracion: %DURATION%s
echo.

REM Filtergraph:
REM - Bosque base: escalar y desaturar ligeramente para efecto brumoso
REM - Bruma animada: capas de ruido blanco/gris con blur para efecto de niebla flotante
REM - Audio: ambiente natural (viento, bosque)

"%FFMPEG%" ^
  -loop 1 -i ".\assets\video\bosque_brumoso.jpg" ^
  -f lavfi -i "color=0x808080:s=%W%x%H%:d=%DURATION%" ^
  -f lavfi -i "anoisesrc=r=44100:c=2:d=%DURATION%" ^
  -filter_complex ^
    "[0:v]scale=%W%:%H%:force_original_aspect_ratio=decrease,pad=%W%:%H%:(ow-iw)/2:(oh-ih)/2,format=rgba,gblur=sigma=0.8[forest];[1:v]fps=%FPS%,noise=alls=20:allf=t,gblur=sigma=4,colorchannelmixer=aa=0.15[mist1];[1:v]fps=15,noise=alls=15:allf=t,gblur=sigma=6,colorchannelmixer=aa=0.1[mist2];[mist1][mist2]blend=all_mode=overlay[mist];[forest][mist]overlay=x=0:y=0,format=yuv420p[final]" ^
  -map "[final]" ^
  -map "2:a" ^
  -c:v mpeg4 -q:v 6 ^
  -c:a aac -ar 44100 -b:a 192k ^
  -t %DURATION% ^
  -r %FPS% ^
  -y "%OUTPUT%"

if %ERRORLEVEL% equ 0 (
    for %%F in ("%OUTPUT%") do set /A SIZE=%%~zF / 1024 / 1024
    echo.
    echo VIDEO GENERADO: BOSQUE BRUMOSO
    echo Archivo: %OUTPUT%
    echo Tamano: !SIZE! MB
    echo Estilo: Bosque denso con niebla flotante
) else (
    echo Error: FFmpeg fallo
    exit /b 1
)
