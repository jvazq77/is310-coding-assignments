# GETting Culture Across APIs

This project uses Riot Data Dragon and the Europeana API to compare game character data with a cultural heritage object.

## APIs Used

### Riot Data Dragon
I used Riot's official Data Dragon API to get data for the League of Legends champion Vi.

### Europeana API
I used the Europeana Record API to get metadata for a historical boxing photograph titled "[Retrat d'un boxejador]" provided by Ajuntament de Girona.

## What the script does

- sends a GET request to Riot Data Dragon
- prints the Riot response
- sends a GET request to the Europeana Record API
- prints the Europeana response
- extracts and cleans specific item data from both APIs
- saves the cleaned data into a JSON file

## Why these items are related

I chose Vi from League of Legends because she is a fighter-type champion known for hand-to-hand combat. I paired that with a historical boxing photograph from Europeana. Both represent fighting and physical combat, which creates a clear cultural connection between a modern video game character and a real-world historical subject.

## Data Cleaning

The Europeana API returns deeply nested data, so I wrote helper functions to extract the correct fields such as title, creator, date, and provider. This ensures the saved JSON file only includes clean and readable item data.

## Files

- `getting_culture.py` — the main Python script  
- `riot_culture_data.json` — the cleaned saved data  
- `README.md` — project explanation  

## Requirements

Install requests:

```bash
pip install requests