from datetime import datetime
import requests
from bs4 import BeautifulSoup as bs
import config as cfg
from lib.email_notification import send_notification
from lib.message import Message
from lib.contact import Contact
from lib.file_handler import file_exists, write_data, read_existing_data

INITIAL_QUERY_URL = cfg.QUERY_URL
BASE_URL = cfg.BASE_URL
HEADERS = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
         AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'}

FILENAME = cfg.PRICE_INFO_FILE_NAME


def main():
    # Initial query
    req = requests.get(INITIAL_QUERY_URL, headers=HEADERS)
    soup = bs(req.text, 'html.parser')

    # Create data dict and fill with existing data if available
    data = {}
    if file_exists(FILENAME):
        data = read_existing_data(FILENAME)

    # Check the website for content
    soup,data = check_pages(req, soup, data)

    # Write data to file for storage
    write_data(FILENAME, data)

    # Check whether there is reason to report something
    changes = check_for_changes(data)

    # Only send Email if there is changes
    if len(changes) > 0:
        changes = structure_report(changes)
        trigger_email('GPU Price Tracker News', changes)


def check_for_changes(data):
    '''
    Compares the previous entries of each individual entry
    and returns the entries where changes occurred
    '''
    new_products = []
    updated_prices = []
    updated_availability = []

    for key, values in data.items():
        if len(values['prices']) == 1:
            new_products.append((values['name'], values['url']))
        else:
            if not values['prices'][-1]['price'] == values['prices'][-2]['price']:
                updated_prices.append(
                    (values['name'], values['prices'][-1]['price'],
                    values['prices'][-2]['price'],
                    values['url']))
            if not values['prices'][-1]['status'] == values['prices'][-2]['status']:
                updated_availability.append(
                    (values['name'], values['prices'][-1]['status'],
                    values['prices'][-2]['status'],
                    values['url']))

    return [new_products, updated_prices, updated_availability]


def structure_report(data):
    '''
    Create a readable string out of the found results
    '''
    report = ''
    # Add new models to result string
    if len(data[0]) > 0:
        report += '\nNew models found: \n'
        for entry in data[0]:
            report += entry[0] + '\n\t' + entry[1] + '\n\n'
    # Add price updates
    if len(data[1]) > 0:
        report += '\nPrices changed for: \n'
        for entry in data[1]:
            report += entry[0] + '\n'
            report += '\t new price: ' + entry[1] + '\n'
            report += '\t old price: ' + entry[2] + '\n'
            report += '\t' + entry[3] + '\n\n'
    # Add status updates
    if len(data[2]) > 0:
        report += '\nAvailability changed for: \n'
        for entry in data[2]:
            report += entry[0] + '\n'
            report += '\t new status: ' + entry[1] + '\n'
            report += '\t old status: ' + entry[2] + '\n'
            report += '\t' + entry[3] + '\n\n'
    return report


def trigger_email(subject, data):
    '''
    Defines the parameters for the email and sends the passed in data
    '''
    # Define basic information for sending automated email notifications
    sender = Contact(cfg.EMAIL_NAME, cfg.EMAIL_ADRESS)

    # Build & Send message
    msg = Message(sender, sender, subject, data)
    send_notification(cfg.SMTP_SERVER, cfg.SMTP_PORT, msg)


def check_pages(req, soup, data):
    '''
    Check the webiste for content and whethere there is multiple pages
    '''
    data = extract_data_entries(soup, data)

    # check if multiple pages exist
    num_pages = soup.find('ul', class_='pagination')
    if not num_pages is None:
        next_page_links = num_pages.find_all('a')
        for i in range(1, len(next_page_links)-1):
            new_query = BASE_URL+next_page_links[i].get('href')
            req = requests.get(new_query, headers=HEADERS)
            soup = bs(req.text, 'html.parser')
            data = extract_data_entries(soup, data)
    return soup, data


def extract_data_entries(soup, data):
    '''
    Find and extract all individual entries (names and prices)
    and return them as dictionary
    '''
    for entry in soup.find_all('li', class_='toggle'):
        product_id = entry.find('small').string
        product_name = entry.find('h2').string
        product_price = entry.find('span', class_='site-currency-lg').string
        product_status = entry.find('div', class_='site-stock-text').string
        product_link = BASE_URL + entry.find('a', class_='site-product-link').get('href')

        if not product_id in data:
            data[product_id] = {'name': product_name, 'prices':[], 'url': product_link}

        data[product_id]['prices'].append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "price": product_price,
                    "status": product_status
                }
            )
    return data


if __name__ == '__main__':
    main()
