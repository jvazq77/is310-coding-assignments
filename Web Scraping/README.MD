# Akshan — League of Legends Fandom Wiki Scraper

## Wiki Chosen
Wiki: League of Legends Wiki on Fandom  
Page scraped: https://leagueoflegends.fandom.com/wiki/Akshan/LoL  
Robots.txt: https://leagueoflegends.fandom.com/robots.txt  
Content license: CC-BY-SA unless otherwise noted

## Terms of Service & robots.txt
Before scraping, I reviewed the robots.txt file for this wiki. I only scraped a normal article page and did not access any restricted or special pages.  

## Why I Chose This Wiki
I chose the Akshan page from the League of Legends Fandom wiki because League of Legends is a well-known game with a large fan community, and Akshan is an interesting champion with clearly organized information on the page. The page includes structured details like his title, release date, classes, position, resource type, and store price, which makes it a good target for a simple web scraping project.

## What Is Being Scraped?
This script collects the following information from the Akshan page:

- `champion_name`
- `champion_title`
- `release_date`
- `classes`
- `positions`
- `resource`
- `range_type`
- `adaptive_type`
- `store_price`

## Why This Data Might Interest Researchers
This data could be useful to researchers studying how fandom communities organize and present structured information about game characters. It could also be useful for research on game design, character categorization, and how fan-made databases document gameplay information. Since champion pages often follow similar patterns, this kind of scraping could also be expanded into a larger dataset for comparing many champions.

## Requirements
- Python 3.7+
- cloudscraper
- beautifulsoup4

Install dependencies with your virtual environment active:

```bash
pip install cloudscraper beautifulsoup4