import re
import unicodedata
from io import StringIO

import pandas as pd
import requests

CSV_IN = 'nba_player_stats.csv'
CSV_OUT = 'nba_player_stats_with_age.csv'
NAME_COL = 'name'

# Basketball Reference names seasons by the year they END: 2026 = 2025-26, 2027 = 2026-27
SEASON_END_YEAR = 2026
BBR_URL = f'https://www.basketball-reference.com/leagues/NBA_{SEASON_END_YEAR}_per_game.html'

# Names that differ between your CSV and Basketball Reference (normalized CSV key -> normalized BBR key)
OVERRIDES = {'ronald holland': 'ron holland'}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/131.0 Safari/537.36'
}


def norm(name: str) -> str:
    """Lowercase, strip accents, punctuation and Jr./Sr./II/III so names match across sites."""
    name = unicodedata.normalize('NFKD', str(name)).encode('ascii', 'ignore').decode()
    name = name.lower().replace('.', '').replace("'", '').replace('-', ' ')
    name = re.sub(r'\b(jr|sr|ii|iii|iv|v)\b', '', name)
    return re.sub(r'\s+', ' ', name).strip()


# --- Pull ages from Basketball Reference (single request) ---
resp = requests.get(BBR_URL, headers=HEADERS, timeout=30)
resp.raise_for_status()
resp.encoding = 'utf-8'   # fixes garbled accented names (Dončić, Jokić, Şengün, ...)

bbr = pd.read_html(StringIO(resp.text), match='Player')[0]
bbr = bbr[bbr['Player'] != 'Player']                        # drop repeated header rows
bbr['Age'] = pd.to_numeric(bbr['Age'], errors='coerce')
bbr = bbr.drop_duplicates(subset='Player', keep='first')    # traded players: combined "2TM/3TM" row comes first
bbr['key'] = bbr['Player'].map(norm)
ages = bbr[['key', 'Age']].rename(columns={'Age': 'AGE'})
print(f"Loaded {len(ages)} players from {BBR_URL}")

# --- Merge into your existing CSV ---
df = pd.read_csv(CSV_IN)
df['key'] = df[NAME_COL].map(norm).replace(OVERRIDES)
out = df.drop(columns=['AGE', 'age'], errors='ignore').merge(ages, on='key', how='left')

missing = out[out['AGE'].isna()][NAME_COL].tolist()
print(f"Matched {len(out) - len(missing)}/{len(out)} players")
if missing:
    print("No age found for:", missing)

out.drop(columns='key').to_csv(CSV_OUT, index=False)
print(f"Saved {CSV_OUT}")