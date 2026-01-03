from PIL import Image
import numpy as np
from pathlib import Path
import sys

# Usage: compare_frames.py frameA.jpg frameB.jpg
if len(sys.argv) >= 3:
    f1 = Path(sys.argv[1])
    f2 = Path(sys.argv[2])
else:
    f1 = Path('out/frame_005.jpg')
    f2 = Path('out/frame_010.jpg')

if not (f1.exists() and f2.exists()):
    print('ERROR: frames missing')
    raise SystemExit(2)

# Load and convert to grayscale for robustness
i1 = np.array(Image.open(f1).convert('L')).astype(float)
i2 = np.array(Image.open(f2).convert('L')).astype(float)

diff = np.abs(i1 - i2)
mad = diff.mean()
maxd = diff.max()
# Fraction of pixels that changed more than a small threshold
th = 6.0
mask = diff > th
frac = mask.mean()
# Mean difference over changing pixels (if any)
mean_change = diff[mask].mean() if mask.any() else 0.0

print(f'mean_abs_diff={mad:.2f}, max_diff={maxd:.1f}, changed_frac={frac:.4f}, mean_change={mean_change:.2f}')

# Decision rules (adjustable): either sizable mean_abs_diff OR a non-trivial fraction of pixels changed noticeably
if mad >= 3.0 or frac >= 0.002:
    print('RESULT: MOVEMENT DETECTED')
    raise SystemExit(0)
else:
    print('RESULT: NO MOVEMENT DETECTED')
    raise SystemExit(3)
