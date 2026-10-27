import time
import urllib.error
import csv
import json
import re
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

URL = 'https://www.lemongym.lt/wp-json/api/async-render-block?pid=NTY3&bid=YWNmL2NsdWJzLW9jY3VwYW5jeQ==&rest_language=en'
FILE = Path('occupancy.csv')
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/156.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.lemongym.lt/en/club-occupancy/",
    "X-Requested-With": "XMLHttpRequest",
}

request = urllib.request.Request(URL, headers=headers)

for attempt in range(3):
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            payload = json.load(response)
        break
    except urllib.error.HTTPError as error:
        if error.code not in (429, 500, 502, 503, 504) or attempt == 2:
            raise
        print(f"HTTP {error.code}; retrying in 20 seconds...")
        time.sleep(20)
html = payload['data']['content']
# Find the specific gym card and its percentage, regardless of other clubs' values.

from html.parser import HTMLParser

class GymParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_card = False
        self.card_depth = 0
        self.card_text = []
        self.cards = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get("class", "").split()

        if tag == "div" and "clubs-occupancy" in classes:
            self.in_card = True
            self.card_depth = 1
            self.card_text = []
        elif self.in_card and tag == "div":
            self.card_depth += 1

    def handle_data(self, data):
        if self.in_card:
            self.card_text.append(data)

    def handle_endtag(self, tag):
        if self.in_card and tag == "div":
            self.card_depth -= 1
            if self.card_depth == 0:
                self.cards.append(" ".join(self.card_text))
                self.in_card = False

parser = GymParser()
parser.feed(html)

percentage = None

for card in parser.cards:
    if "Savanoriai" in card and "168" in card:
        match = re.search(r"(\d+)\s*%", card)
        if match:
            percentage = int(match.group(1))
            break

if percentage is None:
    raise RuntimeError("Could not find Savanoriai occupancy")

now = datetime.now(ZoneInfo('Europe/Vilnius')).isoformat(timespec='seconds')
exists = FILE.exists()
with FILE.open('a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    if not exists or FILE.stat().st_size == 0:
        writer.writerow(['timestamp_lithuania', 'occupancy_percent'])
    writer.writerow([now, percentage])
print(f'{now}: {percentage}%')
