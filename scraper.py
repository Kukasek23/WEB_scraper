"""
Autor: Kukasek23
Email:kukasek2@seznam.cz
"""


import requests
from bs4 import BeautifulSoup as BS
import csv
import sys
import re

BASE_URL = "https://www.volby.cz/pls/ps2017nss/"

def get_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = 'utf-8'
        return response.text
    except requests.RequestException as e:
        print(f"Error loading {url}: {e}", file=sys.stderr)
        sys.exit(1)

def get_municipality_links(url):
    soup = BS(get_html(url), 'html.parser')
    table = soup.find('table')
    municipalities = []

    for row in table.find_all('tr')[2:]:  # Skip header rows
        cells = row.find_all('td')
        if len(cells) >= 3:
            code = cells[0].text.strip()
            name = cells[1].text.strip()
            link = cells[0].find('a')
            if link:
                href = link['href']
                full_url = requests.compat.urljoin(BASE_URL, href)
                municipalities.append((code, name, full_url))

    return municipalities

def parse_municipality_results(url):
    soup = BS(get_html(url), 'html.parser')

    def get_number_by_header(headers):
        cell = soup.find("td", headers=headers)
        return int(cell.text.replace('\xa0', '').replace(' ', '')) if cell else 0

    registered_voters = get_number_by_header("sa2")
    envelopes_issued = get_number_by_header("sa5")
    valid_votes = get_number_by_header("sa6")

    parties = {}
    for table_id in ["t1", "t2"]:
        party_names = soup.find_all("td", class_="overflow_name", headers=f"{table_id}sa1 {table_id}sb2")
        party_votes = soup.find_all("td", class_="cislo", headers=f"{table_id}sa2 {table_id}sb3")

        for name_cell, vote_cell in zip(party_names, party_votes):
            party_name = name_cell.text.strip()
            votes = int(vote_cell.text.replace('\xa0', '').replace(' ', ''))
            parties[party_name] = votes

    return registered_voters, envelopes_issued, valid_votes, parties

def save_to_csv(filename, data, party_names):
    header = ["code", "name", "registered", "envelopes", "valid"] + sorted(party_names)
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=header, delimiter=';')
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def main():
    if len(sys.argv) != 3:
        print("Usage: python scraper.py <url> <output.csv>")
        sys.exit(1)

    url, output_file = sys.argv[1], sys.argv[2]

    if not url.startswith(BASE_URL):
        print(f"URL must start with {BASE_URL}")
        sys.exit(1)

    municipalities = get_municipality_links(url)
    print(f"Found {len(municipalities)} municipalities.")

    results = []
    all_parties = set()

    for idx, (code, name, detail_url) in enumerate(municipalities, 1):
        print(f"[{idx}/{len(municipalities)}] Processing: {name}")
        registered, envelopes, valid, parties = parse_municipality_results(detail_url)
        all_parties.update(parties.keys())
        row = {
            "code": code,
            "name": name,
            "registered": registered,
            "envelopes": envelopes,
            "valid": valid
        }
        row.update(parties)
        results.append(row)

    save_to_csv(output_file, results, all_parties)
    print(f" Results saved to {output_file}")

if __name__ == "__main__":
    main()
