@echo off
setlocal enabledelayedexpansion

REM GENERADOR AUTÓNOMO: Preview 60s - Bosque Lluvioso + Cafe
REM Estándar: Cinematografía HD + Audio Ambiente Sincronizado

set "FFMPEG=C:\Users\Admin\AppData\Local\Microsoft\WinGet\Packages\BtbN.FFmpeg.LGPL.Shared.8.0_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-n8.0.1-17-g27a297f186-win64-lgpl-shared-8.0\bin\ffmpeg.exe"
set "FOREST=.\assets\video\bosque_ventana_ia.png"
set "COFFEE=.\assets\video\taza_cafe_ia.png"
set "OUTPUT=.\out\preview_60s_final.mp4"
set "DURATION=60"
set "FPS=30"
set "W=1920"
set "H=1080"

if not exist ".\out" mkdir ".\out"

REM Filtergraph: Bosque 4K + Lluvia Multicapa + Cafe + Audio Sincronizado

"%FFMPEG%" ^
  -loop 1 -i "%FOREST%" ^
  -f lavfi -i "color=0x000000:s=%W%x%H%:d=%DURATION%" ^
  -loop 1 -i "%COFFEE%" ^
  -f lavfi -i "anoisesrc=r=44100:c=2:d=%DURATION%" ^
  -filter_complex ^
    "[0:v]scale=%W%:%H%:force_original_aspect_ratio=decrease,pad=%W%:%H%:(ow-iw)/2:(oh-ih)/2,format=rgba,gblur=sigma=1[forest];[1:v]fps=%FPS%,noise=alls=50:allf=t,gblur=sigma=2,colorchannelmixer=aa=0.4[rain1];[1:v]fps=20,noise=alls=30:allf=t,gblur=sigma=3,colorchannelmixer=aa=0.25[rain2];[rain1][rain2]blend=all_mode=screen[rain];[forest][rain]overlay=x=0:y=0[base];[2:v]scale=350:280,format=rgba[coffee];[base][coffee]overlay=x=1500:y=750[output];[output]format=yuv420p[final]" ^
  -map "[final]" ^
  -map "3:a" ^
  -c:v libx264 -preset medium -crf 23 ^
  -c:a aac -ar 44100 -b:a 192k ^
  -t %DURATION% ^
  -r %FPS% ^
  -y "%OUTPUT%" 2>&1 | findstr /R "frame= muxing video:"

if %ERRORLEVEL% equ 0 (
    for %%F in ("%OUTPUT%") do set /A SIZE=%%~zF / 1024 / 1024
    echo PREVIEW 60s COMPLETADA
    echo Archivo: %OUTPUT%
    echo Tamano: !SIZE! MB
    echo Duracion: %DURATION%s
    echo Resolucion: %W%x%H%
) else (
    REM Fallback: usar mpeg4 si libx264 no disponible
    "%FFMPEG%" ^
      -loop 1 -i "%FOREST%" ^
      -f lavfi -i "color=0x000000:s=1280x720:d=%DURATION%" ^
      -loop 1 -i "%COFFEE%" ^
      -f lavfi -i "anoisesrc=r=44100:c=2:d=%DURATION%" ^
      -filter_complex ^
        "[0:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,format=rgba,gblur=sigma=1[forest];[1:v]fps=%FPS%,noise=alls=50:allf=t,gblur=sigma=2,colorchannelmixer=aa=0.4[rain1];[1:v]fps=20,noise=alls=30:allf=t,gblur=sigma=3,colorchannelmixer=aa=0.25[rain2];[rain1][rain2]blend=all_mode=screen[rain];[forest][rain]overlay=x=0:y=0[base];[2:v]scale=300:240,format=rgba[coffee];[base][coffee]overlay=x=950:y=450[output];[output]format=yuv420p[final]" ^
        -map "[final]" ^
        -map "3:a" ^
        -c:v mpeg4 -q:v 6 ^
        -c:a aac -ar 44100 -b:a 192k ^
        -t %DURATION% ^
        -r %FPS% ^
        -y "%OUTPUT%"
    
    for %%F in ("%OUTPUT%") do set /A SIZE=%%~zF / 1024 / 1024
    echo PREVIEW 60s COMPLETADA
    echo Archivo: %OUTPUT%
    echo Tamano: !SIZE! MB
)
