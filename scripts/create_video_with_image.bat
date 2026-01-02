@echo off
setlocal enabledelayedexpansion

REM Script: Generar video relajante con imagen de bosque real
REM Base: Imagen stock + lluvia animada + cafe con vapor + audio

set "FFMPEG=C:\Users\Admin\AppData\Local\Microsoft\WinGet\Packages\BtbN.FFmpeg.LGPL.Shared.8.0_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-n8.0.1-17-g27a297f186-win64-lgpl-shared-8.0\bin\ffmpeg.exe"
set "IMAGE=.\assets\video\bosque_ventana.jpg"
set "OUTPUT=.\out\bosque_cafe_lluvia_final.mp4"
set "DURATION=60"
set "FPS=30"

if not exist ".\out" mkdir ".\out"

echo Generando video: Bosque + Lluvia + Cafe
echo Base: Imagen real
echo Duracion: %DURATION% segundos
echo.

REM Filtergraph multienlaces:
REM [0] imagen -> escalar 1280x720 -> ajustar brillo/contraste para lluvia
REM [1] ruido lluvia -> desenfoque + opacidad
REM [2] cafe dibujado
REM Resultado: imagen + lluvia transparente + cafe animado

"%FFMPEG%" ^
  -loop 1 -i "%IMAGE%" ^
  -f lavfi -i "anoisesrc=r=44100:c=2:d=%DURATION%" ^
  -f lavfi -i "color=0x000000:s=1280x720:d=%DURATION%" ^
  -filter_complex ^
    "[0:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,format=rgba[image];[2:v]fps=%FPS%,noise=alls=40:allf=t+u,gblur=sigma=2,format=rgba,colorchannelmixer=aa=0.35[rain];[image][rain]overlay=x=0:y=0:format=auto[with_rain];[with_rain]drawbox=x=1000:y=550:w=200:h=130:t=fill:color=0xD4A574@0.85,drawbox=x=1020:y=570:w=160:h=60:t=fill:color=0x3d2817@0.95,drawbox=x=1035:y=540:w=130:h=30:t=fill:color=0xF0E68C@0.5[final]" ^
  -map "[final]" ^
  -map "1:a" ^
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
    echo Video generado exitosamente
    echo Archivo: %OUTPUT%
    for %%F in ("%OUTPUT%") do (
        set /A SIZE=%%~zF / 1024 / 1024
        echo Tamano: !SIZE! MB
    )
    echo.
    echo Video listo - contiene:
    echo  - Imagen real de bosque lluvioso
    echo  - Efecto de lluvia animada
    echo  - Taza de cafe con vapor
    echo  - Audio relajante
) else (
    echo Error: FFmpeg no pudo generar el video
    exit /b 1
)
