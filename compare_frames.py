#!/usr/bin/env python3
from PIL import Image
import numpy as np
from pathlib import Path
f1=Path('out/frame_005.jpg')
f2=Path('out/frame_010.jpg')
if not (f1.exists() and f2.exists()):
    print('ERROR: frames missing')
    raise SystemExit(2)

i1=np.array(Image.open(f1).convert('RGB')).astype(float)
i2=np.array(Image.open(f2).convert('RGB')).astype(float)
diff=np.abs(i1-i2)
mad=diff.mean()
maxd=diff.max()
print(f'mean_abs_diff={mad:.2f}, max_diff={maxd}')
if mad<3:
    print('RESULT: NO MOVEMENT DETECTED')
    raise SystemExit(3)
else:
    print('RESULT: MOVEMENT DETECTED')
    raise SystemExit(0)
