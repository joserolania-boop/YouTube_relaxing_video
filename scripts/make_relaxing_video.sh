#!/bin/bash
set -euo pipefail

# long-form relaxing video parameters
duration=1800
width=1280
height=720
mkdir -p out

bg_source="color=black:s=${width}x${height}:d=${duration}:r=30"
audio_source="anoisesrc=d=${duration}:r=44100:a=0.4:color=pink"

ffmpeg -y \
  -f lavfi -i "$bg_source" \
  -f lavfi -i "$audio_source" \
  -filter_complex \
    "[0:v]colorchannelmixer=rr=0.6:gg=0.7:bb=0.85,noise=alls=3:allf=t+u,gblur=sigma=4,format=yuv420p[outv]" \
  -map "[outv]" -map 1:a \
  -c:v mpeg4 -q:v 5 -pix_fmt yuv420p \
  -c:a aac -b:a 192k \
  out/relaxing_rain.mp4