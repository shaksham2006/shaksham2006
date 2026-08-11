import json
from pathlib import Path
from datetime import date, timedelta

PALETTE = ['#161b22', '#0e4429', '#006d32', '#26a641', '#39d353', '#69f0a0']
data = json.loads(Path('data/contributions.json').read_text())
days = data.get('days', [])
cells = {d['date']: max(0, min(5, int(d.get('level', 0)))) for d in days}

if days:
    first = date.fromisoformat(days[0]['date'])
    start = first - timedelta(days=first.weekday())
else:
    start = date.today() - timedelta(days=364)
    start -= timedelta(days=start.weekday())

x0, y0, cell, gap = 20, 38, 11, 3
cols, rows = 53, 7
width, height = x0*2 + cols*cell + (cols-1)*gap, 150

rects = []
for c in range(cols):
    for r in range(rows):
        day = start + timedelta(days=c*7+r)
        level = cells.get(day.isoformat(), 0)
        x, y = x0+c*(cell+gap), y0+r*(cell+gap)
        delay = (c+r)*0.012
        rects.append(
            f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2.5" fill="{PALETTE[level]}" opacity="0" transform="translate(-8,-8)">'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.3f}s" dur="0.20s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="-8,-8" to="0,0" begin="{delay:.3f}s" dur="0.28s" fill="freeze"/></rect>'
        )

stats = data.get('stats', {})
total = stats.get('total', sum(int(d.get('count', 0)) for d in days))
streak = stats.get('current_streak', 0)
longest = stats.get('longest_streak', 0)

svg = '<svg xmlns="http://www.w3.org/2000/svg" width="{}" height="{}" viewBox="0 0 {} {}">'.format(width, height, width, height)
svg += '<rect width="100%" height="100%" rx="14" fill="#0d1117" stroke="#30363d"/>'
svg += '<text x="20" y="22" font-family="ui-monospace,monospace" font-size="12" fill="#8b949e">contrib-heatmap - {:,} contributions - streak {} - best {}</text>'.format(total, streak, longest)
svg += ''.join(rects)
svg += '<text x="20" y="132" font-family="ui-monospace,monospace" font-size="10" fill="#8b949e">Less</text>'
for i, color in enumerate(PALETTE):
    svg += '<rect x="{}" y="124" width="11" height="11" rx="2" fill="{}"/>'.format(52+i*18, color)
svg += '<text x="166" y="132" font-family="ui-monospace,monospace" font-size="10" fill="#8b949e">More</text></svg>'

Path('contrib-heatmap.svg').write_text(svg, encoding='utf-8')
print('wrote contrib-heatmap.svg')
