import json
import os
import requests

RIOT_URL = "https://ddragon.leagueoflegends.com/cdn/16.6.1/data/en_US/champion/Vi.json"
EUROPEANA_RECORD_URL = "https://api.europeana.eu/record/v2/2024914/photography_ProvidedCHO_Ajuntament_de_Girona_064512.json"
OUTPUT_FILE = "riot_culture_data.json"


def get_riot_data():
    response = requests.get(RIOT_URL, timeout=15)
    response.raise_for_status()
    return response.json()


def get_europeana_data(api_key):
    params = {"wskey": api_key}
    response = requests.get(EUROPEANA_RECORD_URL, params=params, timeout=15)
    response.raise_for_status()
    return response.json()


def clean_riot_data(riot_data):
    vi_data = riot_data["data"]["Vi"]

    return {
        "id": vi_data.get("id"),
        "name": vi_data.get("name"),
        "title": vi_data.get("title"),
        "partype": vi_data.get("partype"),
        "tags": vi_data.get("tags"),
        "lore": vi_data.get("lore")
    }


def get_nested(data, keys, default=None):
    current = data
    for key in keys:
        if isinstance(key, int):
            if isinstance(current, list) and len(current) > key:
                current = current[key]
            else:
                return default
        else:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
    return current


def first_non_url(values):
    if isinstance(values, list):
        for value in values:
            if isinstance(value, str) and not value.startswith("http"):
                return value
        if values:
            return values[0]
    return values


def find_provider_proxy(proxies):
    for proxy in proxies:
        about = proxy.get("about", "")
        if "/proxy/provider/" in about:
            return proxy
    return {}


def find_aggregator_proxy(proxies):
    for proxy in proxies:
        about = proxy.get("about", "")
        if "/proxy/aggregator/" in about:
            return proxy
    return {}


def find_organization_name(organizations):
    for org in organizations:
        pref = org.get("prefLabel", {})
        if "ca" in pref and pref["ca"]:
            return pref["ca"][0]
        if "en" in pref and pref["en"]:
            return pref["en"][0]
    return None


def clean_europeana_data(europeana_data):
    item = europeana_data.get("object", {})
    proxies = item.get("proxies", [])
    provider_proxy = find_provider_proxy(proxies)
    aggregator_proxy = find_aggregator_proxy(proxies)

    item_id = (
        get_nested(item, ["europeanaAggregation", "aggregatedCHO"])
        or get_nested(item, ["providedCHOs", 0, "about"])
    )

    title = (
        get_nested(provider_proxy, ["dcTitle", "ca", 0])
        or get_nested(provider_proxy, ["dcTitle", "def", 0])
        or get_nested(aggregator_proxy, ["dcTitle", "en", 0])
    )

    creator = first_non_url(
        get_nested(provider_proxy, ["dcCreator", "def"], [])
    )

    date = (
        get_nested(provider_proxy, ["dcDate", "def", 0])
        or get_nested(item, ["timespans", 0, "skosNotation", "def", 0])
    )

    provider = (
        find_organization_name(item.get("organizations", []))
        or get_nested(provider_proxy, ["dcRights", "def", 0])
    )

    country = (
        get_nested(item, ["europeanaAggregation", "edmCountry", "def", 0])
        or get_nested(item, ["places", 1, "prefLabel", "en", 0])
    )

    rights = get_nested(provider_proxy, ["dcRights", "def", 0])

    item_type = item.get("type")

    return {
        "id": item_id,
        "title": title,
        "type": item_type,
        "provider": provider,
        "creator": creator,
        "date": date,
        "country": country,
        "rights": rights
    }


def main():
    europeana_key = os.getenv("EUROPEANA_API_KEY")

    if not europeana_key:
        print("Error: EUROPEANA_API_KEY is not set.")
        print("Set it in your terminal before running the script.")
        return

    print("Getting Riot Data Dragon data...\n")
    riot_data = get_riot_data()
    print(json.dumps(riot_data, indent=2))

    print("\nGetting Europeana record data...\n")
    europeana_data = get_europeana_data(europeana_key)
    print(json.dumps(europeana_data, indent=2))

    cleaned_data = {
        "source_api": "Riot Data Dragon",
        "riot_item": clean_riot_data(riot_data),
        "europeana_item": clean_europeana_data(europeana_data)
    }

    print("\nCleaned Europeana data:")
    print(json.dumps(cleaned_data["europeana_item"], indent=2, ensure_ascii=False))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(cleaned_data, file, indent=2, ensure_ascii=False)

    print(f"\nSaved cleaned item data to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()