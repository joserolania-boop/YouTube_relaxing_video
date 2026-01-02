@echo off
setlocal enabledelayedexpansion

REM Script para generar video relajante: Bosque con lluvia desde ventana con cafe
REM FFmpeg procedural generation

set "FFMPEG=C:\Users\Admin\AppData\Local\Microsoft\WinGet\Packages\BtbN.FFmpeg.LGPL.Shared.8.0_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-n8.0.1-17-g27a297f186-win64-lgpl-shared-8.0\bin\ffmpeg.exe"
set "OUTPUT=.\out\bosque_cafe_final.mp4"
set "DURATION=60"
set "FPS=30"
set "WIDTH=1280"
set "HEIGHT=720"

if not exist ".\out" mkdir ".\out"

echo Generando video: Bosque con lluvia desde ventana con cafe
echo Duracion: %DURATION% segundos
echo Resolucion: %WIDTH%x%HEIGHT%
echo.

REM Filtergraph: fondo bosque + ventana + lluvia + cafe
REM [0] color fondo -> colorchannelmixer (tones) -> gblur (profundidad) -> drawbox (marco ventana) -> drawbox (cafe)
REM [1] color para lluvia -> noise (lluvia) -> gblur -> overlay con [0]

"%FFMPEG%" ^
  -f lavfi -i "color=0x1a3a2a:s=%WIDTH%x%HEIGHT%:d=%DURATION%" ^
  -f lavfi -i "color=0x000000:s=%WIDTH%x%HEIGHT%:d=%DURATION%" ^
  -f lavfi -i "anoisesrc=r=44100:c=2:d=%DURATION%" ^
  -filter_complex ^
    "[0:v]colorchannelmixer=rr=0.35:gg=0.50:bb=0.40:aa=1,gblur=sigma=3,drawbox=x=100:y=80:w=1080:h=600:t=fill:color=0x3a5a4a@0.15,drawbox=x=110:y=90:w=1060:h=580:t=3:color=0x0d1f1a@0.8,drawbox=x=540:y=90:w=2:h=580:t=fill:color=0x0a1810@0.9,drawbox=x=100:y=340:w=1080:h=2:t=fill:color=0x0a1810@0.9,drawbox=x=1020:y=550:w=180:h=120:t=fill:color=0xCCB8A8@0.7,drawbox=x=1040:y=570:w=140:h=60:t=fill:color=0x3d2817@0.9,drawbox=x=1055:y=540:w=110:h=25:t=fill:color=0xf5f5dc@0.6[window];[1:v]fps=%FPS%,noise=alls=35:allf=t+u,gblur=sigma=1.5,format=rgba,colorchannelmixer=aa=0.4[rain];[window][rain]overlay=x=0:y=0[final]" ^
  -map "[final]" ^
  -map "2:a" ^
  -c:v mpeg4 ^
  -q:v 7 ^
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
) else (
    echo Error: FFmpeg no pudo generar el video
    exit /b 1
)
