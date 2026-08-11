from pathlib import Path
Path('info-card.svg').write_text(Path('info-card.svg').read_text(), encoding='utf-8')
print('info-card.svg already contains the generated card')
