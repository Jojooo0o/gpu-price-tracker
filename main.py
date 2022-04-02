
from datetime import datetime
from encodings import utf_8
import json
import requests
from bs4 import BeautifulSoup as bs
from os import path

INITIAL_QUERY_URL = 'https://www.proshop.dk/?pre=0&s=rtx3070&c=grafikkort'
BASE_URL = 'https://www.proshop.dk'
HEADERS = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
         AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'} 

FILENAME = 'gpu_prices.json'

def main():
    req = requests.get(INITIAL_QUERY_URL, headers=HEADERS)
    soup = bs(req.text, 'html.parser')

    print(datetime.now())
    data = {}

    if file_exists(FILENAME):
        data = read_existing_data(FILENAME)

    data = extract_data_entries(soup, data)

    # check if multiple pages exist
    num_pages = soup.find('ul', class_='pagination')
    if not num_pages is None:
        next_page_links = num_pages.find_all('a')
        for i in range(1, len(next_page_links)-1):
            # print(i)
            # print('Link: ', next_page_links[i].get('href'))
            # print(BASE_URL+next_page_links[i].get('href'))
            new_query = BASE_URL+next_page_links[i].get('href')
            req = requests.get(new_query, headers=HEADERS)
            soup = bs(req.text, 'html.parser')
            data = extract_data_entries(soup, data)

    write_data(FILENAME, data)
  

def file_exists(filepath):
    '''
    Validate whether a file exists before trying to open it
    '''
    return True if path.exists(filepath) else False


def write_data(filename, data):
    '''
    Write the collected data to a json file
    '''
    with open(filename, 'w', encoding='utf_8') as file:
        json.dump(data, file, indent=4)


def read_existing_data(filename):
    '''
    Reads historical data from json
    '''
    with open(filename, 'r', encoding='utf_8') as file:
        data = json.load(file)
    return data


def extract_data_entries(soup, data):
    '''
    Find and extract all individual entries (names and prices)
    and return them as dictionary
    '''
    for entry in soup.find_all('li', class_='toggle'): 
        product_name = entry.find('h2').string
        product_price = entry.find('span', class_='site-currency-lg').string

        if not product_name in data:
            data[product_name] = {'prices':[]}

        data[product_name]['prices'].append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "price": product_price
                }
            )
    return data


if __name__ == '__main__':
    main()
