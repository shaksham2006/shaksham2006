from pathlib import Path
import sys
import cv2

src = Path(sys.argv[1] if len(sys.argv) > 1 else 'assets/source-photo.png')
out = Path('data/source-prepped.png')
img = cv2.imread(str(src), cv2.IMREAD_COLOR)
if img is None:
    raise SystemExit(f'Could not read {src}')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.createCLAHE(clipLimit=2.2, tileGridSize=(8, 8)).apply(gray)
gray = cv2.GaussianBlur(gray, (3, 3), 0)
cv2.imwrite(str(out), gray)
print(f'wrote {out}')
