import json
import re
from datetime import date, timedelta
from pathlib import Path
import requests
from bs4 import BeautifulSoup

USERNAME = 'shaksham2006'
url = f'https://github.com/users/{USERNAME}/contributions'
html = requests.get(url, timeout=30, headers={'User-Agent': 'profile-art-refresh/1.0'}).text
soup = BeautifulSoup(html, 'html.parser')

days = []
for cell in soup.select('td[data-date]'):
    ds = cell.get('data-date')
    if not ds:
        continue
    try:
        level = int(cell.get('data-level', '0'))
    except ValueError:
        level = 0
    count = 0
    m = re.search(r'([\\d,]+)\\s+contribution', cell.get('aria-label', ''))
    if m:
        count = int(m.group(1).replace(',', ''))
    days.append({'date': ds, 'count': count, 'level': level})

days.sort(key=lambda x: x['date'])
counts = {d['date']: d['count'] for d in days}
total = sum(counts.values())

current = 0
cursor = date.today()
while counts.get(cursor.isoformat(), 0) > 0:
    current += 1
    cursor -= timedelta(days=1)

longest = best = 0
for d in days:
    if d['count'] > 0:
        best += 1
        longest = max(longest, best)
    else:
        best = 0

payload = {
    'username': USERNAME,
    'days': days,
    'stats': {'total': total, 'current_streak': current, 'longest_streak': longest}
}
Path('data/contributions.json').write_text(json.dumps(payload, indent=2), encoding='utf-8')
print(f'saved {len(days)} days')

