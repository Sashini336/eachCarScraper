import requests
from bs4 import BeautifulSoup
import json

def extract_info(soup):
    year = None
    millage = None
    fuel_type = None
    transmission = None
    horsepower = None
    engine_liters = None
    doors = None
    color = None

    ul_element = soup.find('div', class_='options-left').find('ul')
    if ul_element:
        li_items = ul_element.find_all('li')

        try:
            year = li_items[0].text.strip()
        except IndexError:
            pass

        try:
            millage = li_items[1].text.strip()
        except IndexError:
            pass

        try:
            fuel_type = li_items[2].text.strip()
        except IndexError:
            pass

        try:
            transmission = li_items[3].text.strip()
        except IndexError:
            pass

    ul_element_right = soup.find('div', class_='options-right').find('ul')
    if ul_element_right:
        li_items_right = ul_element_right.find_all('li')

        try:
            horsepower = li_items_right[0].text.strip()
        except IndexError:
            pass

        try:
            engine_liters = li_items_right[1].text.strip()
        except IndexError:
            pass

        try:
            doors = li_items_right[2].text.strip()
        except IndexError:
            pass

        try:
            color = li_items_right[3].text.strip()
        except IndexError:
            pass

    return {
        'year': year,
        'millage': millage,
        'fuel_type': fuel_type,
        'transmission': transmission,
        'horsepower': horsepower,
        'engine_liters': engine_liters,
        'doors': doors,
        'color': color
    }

def scrape_single_ad(link):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }

        response = requests.get(link, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        info = extract_info(soup)
        return info

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the website: {e}")
        return None

def scrape_and_save_to_json(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as file:
        data = json.load(file)

    scraped_data = []
    for item in data:
        link = item['path']
        info = scrape_single_ad(link)
        if info:
            scraped_data.append(info)

    with open(output_filename, 'w', encoding='utf-8') as file:
        json.dump(scraped_data, file, ensure_ascii=False, indent=4)

    print("Scraping and saving to JSON completed!")

if __name__ == "__main__":
    input_filename = "data.json"
    output_filename = "scraped_data.json"
    scrape_and_save_to_json(input_filename, output_filename)
