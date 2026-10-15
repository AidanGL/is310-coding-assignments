import requests
import json
URL = "https://lotr.fandom.com/api.php"

params = {
    "action": "query",
    "list": "search",
    "srsearch": "dragon",
    "format": "json",
}

response = requests.get(URL, params=params)
response.raise_for_status()



data = response.json()

# Keep only useful information from each matching page
wiki_items = [
    {
        "title": result["title"],
        "pageid": result["pageid"],
        "snippet": result["snippet"]
    }
    for result in data.get("query", {}).get("search", [])
]

# Print the selected results
print(json.dumps(wiki_items, indent=2))

# Save only the selected page data
with open("lotr_wiki_search.json", "w", encoding="utf-8") as file:
    json.dump(wiki_items, file, indent=2)

print("Saved LOTR Wiki search data.")