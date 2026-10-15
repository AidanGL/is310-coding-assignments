
import requests
import json

# Met Museum API endpoints
SEARCH_URL = (
    "https://collectionapi.metmuseum.org/public/collection/v1.1/search"
)
OBJECT_URL = (
    "https://collectionapi.metmuseum.org/public/collection/v1/objects"
)

# 1. Search for dragon-related artwork
params = {
    "q": "dragon",
    "hasImages": "true",
    "limit": 10
}

try:
    response = requests.get(
        SEARCH_URL,
        params=params,
        timeout=20
    )

    if response.status_code != 200:
        print("Search failed:", response.status_code)
        print(response.text)

    else:
        search_data = response.json()
        object_ids = search_data.get("objectIDs") or []

        print("Total matching artworks:", search_data.get("total", 0))

        if object_ids:
            # Try results until one artwork can be retrieved
            artwork = None

            for object_id in object_ids:
                artwork_response = requests.get(
                    f"{OBJECT_URL}/{object_id}",
                    timeout=20
                )

                if artwork_response.status_code == 200:
                    artwork = artwork_response.json()
                    break

                print(
                    "Could not retrieve object",
                    object_id,
                    "- Status:",
                    artwork_response.status_code
                )

            if artwork:
                # 2. Keep only useful artwork fields
                item_data = {
                    "objectID": artwork.get("objectID"),
                    "title": artwork.get("title"),
                    "artist": artwork.get("artistDisplayName"),
                    "date": artwork.get("objectDate"),
                    "medium": artwork.get("medium"),
                    "culture": artwork.get("culture"),
                    "image": artwork.get("primaryImage"),
                    "museum_url": artwork.get("objectURL")
                }

                # 3. Print the selected artwork
                print("\nSelected artwork:")
                print(json.dumps(item_data, indent=2))

                # 4. Save only the selected artwork data
                with open(
                    "met_artwork.json",
                    "w",
                    encoding="utf-8"
                ) as file:
                    json.dump(item_data, file, indent=2)

                print("\nSaved artwork to met_artwork.json")

            else:
                print("No artwork records could be retrieved.")

        else:
            print("No matching artworks found.")

except requests.RequestException as error:
    print("Network error:", error)

except ValueError as error:
    print("Could not parse JSON:", error)
