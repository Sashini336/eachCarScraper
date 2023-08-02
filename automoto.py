import requests
from bs4 import BeautifulSoup
import json
import os

def extract_more_information(soup):
    more_information = []

    title_info_div = soup.find_all('div', class_='col-md-12')[3]
    br_elements = title_info_div.find_all('br')
    for br in br_elements:
        info = br.next_sibling.strip()
        more_information.append(info)

    return more_information

def extract_info(soup):
    title = None
    year = None
    millage = None
    fuel_type = None
    transmission = None
    horsepower = None
    engine_liters = None
    doors = None
    color = None

    # Extract the title
    title_element = soup.find('h1', class_='post-title')
    title = title_element.text.strip() if title_element else None

    article_element = soup.find('article', class_='single-vehicle-details')
    row_element = article_element.find('div', class_='row')
    col_md_6_element = row_element.find_all('div', class_='col-md-6')[5]
    row_2_element = col_md_6_element.find_all('div', class_='column')

    image_urls = []

    for div in row_2_element:
        img_tag = div.find('img')
        if img_tag and 'src' in img_tag.attrs:
            image_url = img_tag['src']
            image_urls.append(image_url)

    # Extract the more information
    more_information = extract_more_information(soup)

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
        'id': None,  # Placeholder for the 'id' field
        'title': title,
        #'price': price,
        'year': year,
        'millage': millage,
        'fuel_type': fuel_type,
        'transmission': transmission,
        'horsepower': horsepower,
        'engine_liters': engine_liters,
        'doors': doors,
        'color': color,
        'image_urls': image_urls,  # Add the 'image_urls' field to the dictionary
        'moreInformation': more_information
    }

def scrape_single_ad(link, ad_id):
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
        info['id'] = ad_id
        return info

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the website: {e}")
        return None

def scrape_and_save_to_json(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as file:
        data = json.load(file)

    scraped_data = []
    for ad_id, item in enumerate(data, start=1):
        link = item['path']
        info = scrape_single_ad(link, ad_id)
        if info:
            scraped_data.append(info)

    # Custom output directory and file name
    output_directory = "output_data"
    output_filename = os.path.join(output_directory, output_filename)

    os.makedirs(output_directory, exist_ok=True)

    with open(output_filename, 'w', encoding='utf-8') as file:
        json.dump(scraped_data, file, ensure_ascii=False, indent=4)

    print("Scraping and saving to JSON completed!")

if __name__ == "__main__":
    input_filename = "data.json"
    output_filename = "scraped_data.json"

    custom_output_directory = "/Users/a.petkov/Desktop/reworkedv2/json"
    custom_output_filename = "data.json"
    scrape_and_save_to_json(input_filename, os.path.join(custom_output_directory, custom_output_filename))
