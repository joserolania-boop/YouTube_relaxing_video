#!/bin/bash
echo "Checking ffmpeg version:"
ffmpeg -version | head -1
echo ""
echo "Checking ffprobe version:"
ffprobe -version | head -1
echo ""
echo "Checking python presence:"
if command -v python &> /dev/null; then
    python --version
else
    echo "Python not found"
fi