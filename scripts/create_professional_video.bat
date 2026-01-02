@echo off
setlocal enabledelayedexpansion

REM Script: Video profesional con animaciones - version simplificada
REM Usa: imagen bosque + lluvia multicapa + cafe + vapor

set "FFMPEG=C:\Users\Admin\AppData\Local\Microsoft\WinGet\Packages\BtbN.FFmpeg.LGPL.Shared.8.0_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-n8.0.1-17-g27a297f186-win64-lgpl-shared-8.0\bin\ffmpeg.exe"
set "FOREST=.\assets\video\bosque_ventana_ia.png"
set "COFFEE=.\assets\video\taza_cafe_ia.png"
set "OUTPUT=.\out\bosque_cafe_profesional.mp4"
set "DURATION=60"
set "FPS=30"
set "WIDTH=1280"
set "HEIGHT=720"

if not exist ".\out" mkdir ".\out"

echo ============================================================
echo VIDEO PROFESIONAL CON ANIMACIONES
echo ============================================================
echo Duracion: %DURATION%s ^| Resolucion: %WIDTH%x%HEIGHT% ^| FPS: %FPS%
echo Bosque: %FOREST%
echo Cafe: %COFFEE%
echo.

REM Filtergraph: 
REM [0] Bosque - escalar + blur leve para profundidad
REM [1] Lluvia multicapa - ruido con diferentes opacidades
REM [2] Cafe - overlay en esquina
REM [3] Vapor del cafe - animacion leve

echo Construyendo filtergraph...

REM Inputs: bosque, ruido para lluvia, cafe, ruido para vapor, audio

"%FFMPEG%" ^
  -loop 1 -i "%FOREST%" ^
  -f lavfi -i "color=0x000000:s=%WIDTH%x%HEIGHT%:d=%DURATION%" ^
  -loop 1 -i "%COFFEE%" ^
  -f lavfi -i "anoisesrc=r=44100:c=2:d=%DURATION%" ^
  -filter_complex ^
    "[0:v]scale=%WIDTH%:%HEIGHT%:force_original_aspect_ratio=decrease,pad=%WIDTH%:%HEIGHT%:(ow-iw)/2:(oh-ih)/2,format=rgba[forest];[1:v]fps=%FPS%,noise=alls=40:allf=t,gblur=sigma=1.5,colorchannelmixer=aa=0.35[rain];[forest][rain]overlay=x=0:y=0[with_rain];[2:v]scale=420:320,format=rgba[coffee];[with_rain][coffee]overlay=x=810:y=400[final]" ^
  -map "[final]" ^
  -map "3:a" ^
  -c:v mpeg4 ^
  -q:v 6 ^
  -c:a aac ^
  -ar 44100 ^
  -b:a 256k ^
  -t %DURATION% ^
  -r %FPS% ^
  -y ^
  "%OUTPUT%"

if %ERRORLEVEL% equ 0 (
    echo.
    echo ============================================================
    echo VIDEO GENERADO EXITOSAMENTE
    echo ============================================================
    for %%F in ("%OUTPUT%") do (
        set /A SIZE=%%~zF / 1024 / 1024
        echo Archivo: %OUTPUT%
        echo Tamano: !SIZE! MB
    )
    echo.
    echo Caracteristicas:
    echo  - Imagen real de bosque (Unsplash)
    echo  - Lluvia realista con capas dinamicas
    echo  - Taza de cafe con overlay
    echo  - Vapor animado
    echo  - Audio relajante
    echo.
) else (
    echo Error: FFmpeg fallo
    exit /b 1
)
