from pathlib import Path
from PIL import Image, ImageEnhance

img = ImageEnhance.Contrast(Image.open('data/source-prepped.png').convert('L')).enhance(1.55)
cols = 92
rows = max(1, int(img.height / img.width * cols * 0.50))
img = img.resize((cols, rows), Image.Resampling.LANCZOS)
ramp = ' .`:-=+*cs#%@'
lines = []

for y in range(rows):
    s = ''
    for x in range(cols):
        v = img.getpixel((x, y))
        if v > 225:
            s += ' '
        else:
            i = max(0, min(len(ramp)-1, int((255-v)/256*len(ramp))))
            s += ramp[i]
    lines.append(s.rstrip())

while lines and not lines[0].strip():
    lines.pop(0)
while lines and not lines[-1].strip():
    lines.pop()

W, H = 940, len(lines)*10+24
parts = []
for i, line in enumerate(lines):
    safe = line.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
    y = 18+i*10
    delay = i*0.055
    parts.append(
        '<g opacity="0">'
        f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.3f}s" dur="0.18s" fill="freeze"/>'
        f'<clipPath id="clip{i}"><rect x="0" y="{y-9}" width="0" height="12">'
        f'<animate attributeName="width" from="0" to="{W}" begin="{delay:.3f}s" dur="0.70s" fill="freeze"/></rect></clipPath>'
        f'<text x="4" y="{y}" font-family="ui-monospace,monospace" font-size="9" fill="#c9d1d9" xml:space="preserve" clip-path="url(#clip{i})">{safe}</text>'
        '</g>'
    )

svg = '<svg xmlns="http://www.w3.org/2000/svg" width="{}" height="{}" viewBox="0 0 {} {}">'.format(W,H,W,H)
svg += '<rect width="100%" height="100%" rx="12" fill="#0d1117"/>'
svg += '<text x="14" y="13" font-family="ui-monospace,monospace" font-size="8" fill="#8b949e">portrait.render --mode ascii</text>'
svg += ''.join(parts) + '</svg>'
Path('avi-ascii.svg').write_text(svg, encoding='utf-8')
print('wrote avi-ascii.svg')
