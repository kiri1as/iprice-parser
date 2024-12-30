import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import List, Union

import requests
from bs4 import BeautifulSoup

from constants import PHONES_BASE_URL, APPLE_PRODUCER_PARAM
from db import Session
from model import Product, ProductRecordType

logger = logging.getLogger(__name__)


def update_products_data(scheduled=False):
    logger.info(f'--- PROCESSING PRODUCTS PRICES STARTED ---')

    base_url = f'{PHONES_BASE_URL}/{APPLE_PRODUCER_PARAM}'
    products, cnt = process_product_page(base_url, page_counter=True, scheduled=scheduled)

    if cnt > 0:
        urls = [f'{PHONES_BASE_URL}page={p};{APPLE_PRODUCER_PARAM}' for p in range(2, cnt + 1)]

        with ThreadPoolExecutor(max_workers=6) as executor:
            product_pages = list(
                executor.map(lambda url: process_product_page(page_url=url, scheduled=scheduled),
                             urls))
            for page in product_pages:
                save_products(page)

    logger.info(f'--- PROCESSING PRODUCTS PRICES ENDED ---')


def process_product_page(page_url: str, page_counter=False, scheduled=False) -> Union[
    List[Product], tuple[List[Product], int]]:
    logger.info(f' ... Processing page: {page_url} ... ')

    products = []
    r = requests.get(page_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    tiles = soup.find_all("rz-catalog-tile")

    for tile in tiles:
        old_price_tag = tile.find(name='div', attrs={'class': 'goods-tile__price--old'})
        new_price_tag = tile.find(name='div', attrs={'class': 'goods-tile__price'})

        old_price_value = int(old_price_tag.contents[0].strip().replace('\xa0', '')) if old_price_tag else None
        old_price_curr = old_price_tag.findChild(name='span',
                                                 attrs={'class': 'currency'}).text.strip() if old_price_tag else None
        new_price_value = int(new_price_tag.findChild(name='span', attrs={'class': 'goods-tile__price-value'}).contents[
                                  0].strip().replace('\xa0', '')) if new_price_tag else None
        new_price_curr = new_price_tag.findChild(name='span',
                                                 attrs={'class': 'currency'}).text.strip() if new_price_tag else None

        product_data = {
            'record_type': ProductRecordType.auto if scheduled else ProductRecordType.manual,
            'product_id': tile.find(attrs={'class': 'g-id'}).text.strip(),
            'product_name': tile.find(attrs={'class': 'goods-tile__title'}).text.strip(),
            'product_status': tile.find(attrs={'class': 'goods-tile__availability'}).text.strip(),
            'product_price_old': old_price_value,
            'product_price_old_curr': old_price_curr,
            'product_price_new': new_price_value,
            'product_price_new_curr': new_price_curr,
        }
        products.append(Product(**product_data))

    if page_counter:
        pagination_tag = soup.find('rz-paginator')
        page_count = int(pagination_tag.findChildren('li')[-1].text) if pagination_tag else 0
        return products, page_count
    else:
        return products


def save_products(products: List[Product]):
    with Session() as session:
        session.add_all(products)
        session.commit()
