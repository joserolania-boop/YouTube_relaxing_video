@echo off
setlocal enabledelayedexpansion

REM CALIDAD ASEGURADA: Bosque Brumoso Profesional
REM Basado en: Frame de referencia (bosque verde denso + niebla blanca)

set "FFMPEG=C:\Users\Admin\AppData\Local\Microsoft\WinGet\Packages\BtbN.FFmpeg.LGPL.Shared.8.0_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-n8.0.1-17-g27a297f186-win64-lgpl-shared-8.0\bin\ffmpeg.exe"
set "FOREST=.\assets\video\bosque_brumoso.jpg"
set "OUTPUT=.\out\bosque_brumoso_v2.mp4"
set "DURATION=60"
set "FPS=30"

echo ===============================================
echo CONTROL DE CALIDAD: Bosque Brumoso
echo ===============================================
echo Verificando imagen base...

if not exist "%FOREST%" (
    echo ERROR: Imagen no encontrada - %FOREST%
    exit /b 1
)

for %%F in ("%FOREST%") do (
    set /A SIZE_KB=%%~zF / 1024
    echo OK: Imagen encontrada (!SIZE_KB! KB)
)

echo.
echo Analizando imagen con FFmpeg...
"%FFMPEG%" -i "%FOREST%" 2>&1 | findstr /R "Duration|Video:"

echo.
echo Generando video...
echo.

REM Filtergraph MEJORADO:
REM - Imagen real como base
REM - Brillo y contraste ajustado
REM - Capas de niebla blanca (no gris)
REM - Audio ambiente

"%FFMPEG%" ^
  -loop 1 -i "%FOREST%" ^
  -f lavfi -i "color=0xffffff:s=1280x720:d=%DURATION%" ^
  -f lavfi -i "anoisesrc=r=44100:c=2:d=%DURATION%" ^
  -filter_complex ^
    "[0:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,format=rgba,gblur=sigma=1[forest];[1:v]fps=%FPS%,noise=alls=15:allf=t,gblur=sigma=5,colorchannelmixer=aa=0.12[mist_light];[forest][mist_light]overlay=x=0:y=0:format=auto,format=yuv420p[final]" ^
  -map "[final]" ^
  -map "2:a" ^
  -c:v mpeg4 -q:v 5 ^
  -c:a aac -ar 44100 -b:a 192k ^
  -t %DURATION% ^
  -r %FPS% ^
  -y "%OUTPUT%"

if %ERRORLEVEL% equ 0 (
    echo.
    echo ===============================================
    echo VERIFICACION DE SALIDA
    echo ===============================================
    
    for %%F in ("%OUTPUT%") do (
        set /A SIZE_MB=%%~zF / 1024 / 1024
        set "MOD_TIME=%%~tF"
        echo Video: %%~nxF
        echo Tamano: !SIZE_MB! MB
        echo Creado: !MOD_TIME!
    )
    
    echo.
    echo Extrayendo frame de verificacion...
    "%FFMPEG%" -i "%OUTPUT%" -ss 00:00:30 -vframes 1 -q:v 2 -y ".\out\check_frame.jpg" 2>&1 | findstr /v "ffmpeg\|configuration\|libav"
    
    if exist ".\out\check_frame.jpg" (
        echo OK: Frame de referencia guardado en out\check_frame.jpg
        echo.
        echo VERIFICAR VISUALMENTE:
        echo - ^>Verde oscuro con arboles densosZ
        echo - ^>Niebla blanca flotante
        echo - ^>NO gris monotonico
        echo - ^>Profundidad y atmosfera
    )
    
    echo.
    echo VIDEO LISTO: %OUTPUT%
    
) else (
    echo ERROR: FFmpeg fallo
    exit /b 1
)
