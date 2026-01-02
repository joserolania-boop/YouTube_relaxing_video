#!/usr/bin/env python3
"""Verifica que `out/preview_frame.jpg` no sea una imagen uniforme (gris/negra/blanca)"""
from pathlib import Path
from PIL import Image
import numpy as np
import sys

IMG = Path("out/preview_frame.jpg")
if not IMG.exists():
    print("ERROR: no existe out/preview_frame.jpg")
    sys.exit(2)

img = Image.open(IMG).convert("RGB")
arr = np.array(img).astype(np.float32)

# Luminance
lum = 0.299 * arr[..., 0] + 0.587 * arr[..., 1] + 0.114 * arr[..., 2]
mean_lum = lum.mean()
std_lum = lum.std()

# Colorfulness proxy: mean of channel stddevs
color_std = arr.std(axis=(0,1)).mean()

print(f"mean_lum={mean_lum:.2f}, std_lum={std_lum:.2f}, color_std={color_std:.2f}")

# Heuristics tuned by eyeballing results
if std_lum < 8 or color_std < 6:
    print("RESULT: FAIL - imagen demasiado uniforme o gris/negra/blanca")
    sys.exit(3)
else:
    print("RESULT: PASS - imagen aparentemente válida")
    sys.exit(0)
