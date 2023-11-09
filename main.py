import requests
from bs4 import BeautifulSoup
import telebot
from loguru import logger
import time

# URL to be scraped
psp_url = 'https://www.olx.kz/elektronika/igry-i-igrovye-pristavki/pristavki/pavlodar/?search%5Border%5D=created_at:desc&search%5Bfilter_enum_console_manufacturers%5D%5B0%5D=2273'
playstation_url = 'https://www.olx.kz/elektronika/igry-i-igrovye-pristavki/pristavki/pav/?search%5Bfilter_enum_console_manufacturers%5D%5B0%5D=2272&search%5Border%5D=created_at%3Adesc'
graphic_cards_url = 'https://www.olx.kz/elektronika/kompyutery-i-komplektuyuschie/komplektuyuschie-i-aksesuary/pavlodar/?search%5Bfilter_enum_subcategory%5D%5B0%5D=videokarty&search%5Border%5D=created_at%3Adesc'
TG_TOKEN = ''
TG_ID = 


def send_msg(msg):
    try:
        bot = telebot.TeleBot(TG_TOKEN)
        bot.send_message(TG_ID, msg)
    except Exception as error:
        logger.error(error)

# Get the page
def get_page_data(page_url):
    try:
        full_page = requests.get(page_url)
        soup = BeautifulSoup(full_page.content, 'html.parser')
        table = soup.find_all("div", {"data-testid": "listing-grid"})
        rows = table[0].find_all('div', {'data-cy': 'l-card'})
        result = []
        for row in rows:
            price = row.find('p', {'data-testid': 'ad-price', 'class': 'css-10b0gli er34gjf0'}).text
            name = row.find('h6', {'class': 'css-16v5mdi er34gjf0'}).text
            if page_url == playstation_url:
                name_splitted = name.split(' ')
                if '5' not in name_splitted:
                    continue
            url = row.find('a', {'class': 'css-rc5s2u'}).get('href')
            item_url = f'https://www.olx.kz/{url}'
            item = f'{name} - {price} - {item_url}'
            result.append(item)
        return result
    except requests.exceptions.RequestException as error:
        logger.error(error)
        return []  # Return an empty list if there's an error

def main():
    logger.info('Start')
    last_items_graphic_cards = set()
    last_items_psp = set()
    last_items_playstation = set()
    while True:
        try:
            result_graphic_cards = get_page_data(graphic_cards_url)
            new_items_graphic_cards = []
            for item in result_graphic_cards:
                if item not in last_items_graphic_cards:
                    new_items_graphic_cards.append(item)
                    last_items_graphic_cards.add(item)

            if new_items_graphic_cards:
                for item in reversed(new_items_graphic_cards):
                    send_msg(item)
            time.sleep(2)

            result_psp = get_page_data(psp_url)
            new_items_psp = []
            for item in result_psp:
                if item not in last_items_psp:
                    new_items_psp.append(item)
                    last_items_psp.add(item)

            if new_items_psp:
                for item in reversed(new_items_psp):
                    send_msg(item)
            time.sleep(1)

            result_playstation = get_page_data(playstation_url)
            new_items_playstation = []
            for item in result_playstation:
                if item not in last_items_playstation:
                    new_items_playstation.append(item)
                    last_items_playstation.add(item)
                
            if new_items_playstation:
                for item in reversed(new_items_playstation):
                    send_msg(item)  
            time.sleep(1)    
        except Exception as error:
            logger.error(error)
            time.sleep(10) 

main()
