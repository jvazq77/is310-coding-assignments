from bs4 import BeautifulSoup
import cloudscraper
import csv
import os

URL = "https://leagueoflegends.fandom.com/wiki/Akshan/LoL"
OUTPUT_FILE = "akshan_lol_data.csv"

scraper = cloudscraper.create_scraper()


def fetch_page(url):
    response = scraper.get(url, timeout=10)
    response.raise_for_status()
    return response


def clean_lines(text):
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if line:
            lines.append(line)
    return lines


def get_value_after_label(lines, label):
    for i, line in enumerate(lines):
        if line == label and i + 1 < len(lines):
            return lines[i + 1]
    return ""


def get_multiple_values_between(lines, start_label, stop_label):
    values = []
    collecting = False

    for line in lines:
        if line == start_label:
            collecting = True
            continue

        if collecting:
            if line == stop_label:
                break
            values.append(line)

    return values


def parse_akshan_data(response):
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text("\n", strip=True)
    lines = clean_lines(text)

    champion_name = "Akshan"
    champion_title = "the Rogue Sentinel"

    release_date = get_value_after_label(lines, "Release date")
    positions = get_multiple_values_between(lines, "Position(s)", "Resource")
    classes = get_multiple_values_between(lines, "Class(es)", "Legacy")
    resource = get_value_after_label(lines, "Resource")
    range_type = get_value_after_label(lines, "Range type")
    adaptive_type = get_value_after_label(lines, "Adaptive type")
    store_price = get_value_after_label(lines, "Store price")

    data = {
        "champion_name": champion_name,
        "champion_title": champion_title,
        "release_date": release_date,
        "classes": ", ".join(classes),
        "positions": ", ".join(positions),
        "resource": resource,
        "range_type": range_type,
        "adaptive_type": adaptive_type,
        "store_price": store_price
    }

    return data


def save_to_csv(data, filename):
    filepath = os.path.abspath(filename)

    with open(filepath, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "champion_name",
            "champion_title",
            "release_date",
            "classes",
            "positions",
            "resource",
            "range_type",
            "adaptive_type",
            "store_price"
        ])
        writer.writerow([
            data["champion_name"],
            data["champion_title"],
            data["release_date"],
            data["classes"],
            data["positions"],
            data["resource"],
            data["range_type"],
            data["adaptive_type"],
            data["store_price"]
        ])

    print(f"Saved to: {filepath}")


def preview_data(data):
    print("\nPreview of scraped data:")
    for key, value in data.items():
        print(f"{key}: {value}")


def main():
    print("League of Legends Fandom Wiki Scraper")
    print("Scraping Akshan page...\n")

    response = fetch_page(URL)
    data = parse_akshan_data(response)
    preview_data(data)
    save_to_csv(data, OUTPUT_FILE)


if __name__ == "__main__":
    main()