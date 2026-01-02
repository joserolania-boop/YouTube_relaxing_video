#!/bin/bash
ffmpeg -f lavfi -i "anoisesrc=d=20:r=44100:a=0.3:color=pink" -af "highpass=f=1000,lowpass=f=3000,volume=0.7" -c:a aac assets/audio/rain_sound.aac