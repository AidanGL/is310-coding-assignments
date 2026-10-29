
import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin

BASE_URL = "https://bulbapedia.bulbagarden.net"
LIST_URL = BASE_URL + (
    "/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number"
)

HEADERS = {
    "User-Agent": "IS310StudentProject/1.0 (educational web scraping)"
}


def get_soup(url):
    response = requests.get(url, headers=HEADERS, timeout=15)
    print("Status:", response.status_code, url)

    if response.status_code != 200:
        return None

    return BeautifulSoup(response.text, "html.parser")


# LEVEL 1: Get Pokémon from the listing page.
soup = get_soup(LIST_URL)
pokemon_list = []

if soup:
    for table in soup.find_all("table"):
        for row in table.find_all("tr"):
            cells = row.find_all("td", recursive=False)

            if len(cells) < 4:
                continue

            number = cells[0].get_text(" ", strip=True)

            if not number.startswith("#"):
                continue

            # Find the Pokémon's own article link.
            name_link = None

            for link in cells[2].find_all("a", href=True):
                if link["href"].startswith("/wiki/"):
                    name_link = link
                    break

            if name_link is None:
                continue

            name = name_link.get_text(" ", strip=True)
            page_url = urljoin(BASE_URL, name_link["href"])

            types = ", ".join(
                cell.get_text(" ", strip=True)
                for cell in cells[3:]
                if cell.get_text(" ", strip=True)
            )

            pokemon_list.append({
                "number": number.lstrip("#"),
                "name": name,
                "types": types,
                "url": page_url
            })

            if len(pokemon_list) == 10:
                break

        if len(pokemon_list) == 10:
            break

print("Pokémon found:", len(pokemon_list))

# LEVEL 2: Visit individual Pokémon pages.
results = []

for pokemon in pokemon_list:
    time.sleep(5)

    detail_soup = get_soup(pokemon["url"])
    description = ""

    if detail_soup:
        content = detail_soup.find(
            "div", id="mw-content-text"
        )

        if content:
            for paragraph in content.find_all("p"):
                text = paragraph.get_text(" ", strip=True)

                if text:
                    description = text
                    break

    results.append({
        "number": pokemon["number"],
        "name": pokemon["name"],
        "types": pokemon["types"],
        "description": description,
        "url": pokemon["url"]
    })

    print("Collected:", pokemon["name"])

# Save the collected data.
with open(
    "bulbapedia_pokemon.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:
    columns = [
        "number", "name", "types", "description", "url"
    ]

    writer = csv.DictWriter(file, fieldnames=columns)
    writer.writeheader()
    writer.writerows(results)

print("Saved", len(results), "Pokémon to CSV.")
