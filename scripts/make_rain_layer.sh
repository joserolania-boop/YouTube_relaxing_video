#!/bin/bash
ffmpeg -f lavfi -i "color=black:s=1920x1080:d=20:r=30" -vf "frei0r=rain:0.5" -c:v libx264 -preset fast -crf 22 -pix_fmt yuva420p assets/video/rain_loop.mp4