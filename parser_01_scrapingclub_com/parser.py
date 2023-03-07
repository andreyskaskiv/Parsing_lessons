from typing import Generator, NamedTuple

import requests
from bs4 import BeautifulSoup as BS
from tqdm import tqdm

from definitions import PATH_TO_GOODS
from parser_01_scrapingclub_com.tools.check_time import check_time
from parser_01_scrapingclub_com.tools.utils import change_user_agent, get_full_url_domain_name, write_to_json


class GoodsDTO(NamedTuple):
    name: str
    price: str
    description: str
    url_img: str


def get_link_to_card(headers: dict, full_url_domain_name: str, url_site: str, ):
    """ returns a link to the product cards in on page """

    for page_number in range(1, 7):
        url = f"{url_site}{page_number}"
        response = requests.get(url, headers=headers)
        soup = BS(response.text, "lxml")
        product_cards = soup.find_all("div", class_="col-lg-4 col-md-6 mb-4")

        for product_card in product_cards:
            card_link = f"{full_url_domain_name}{product_card.find('a').get('href')}"
            yield card_link


def prepare_card_details(headers: dict, full_url_domain_name: str, card_url: Generator):
    cards_prepared_to_json = []

    num_cards = len(list(card_url))
    card_url = get_link_to_card(headers, full_url_domain_name, url_site)  # reset generator

    with tqdm(total=num_cards, unit="card", desc="Processing", colour='green') as progress_bar:
        for card in card_url:
            response = requests.get(card, headers=headers)
            soup = BS(response.text, "lxml")

            data = soup.find("div", class_="card mt-4 my-4")

            name_product = data.find("h3", class_="card-title").text
            price_product = data.find("h4").text
            info_product = data.find("p", class_="card-text").text
            url_img_product = f'{full_url_domain_name}{data.find("img", class_="card-img-top img-fluid").get("src")}'

            temp = {
                'name': name_product,
                'price': price_product,
                'description': info_product,
                'url_img': url_img_product
            }
            cards_prepared_to_json.append(temp)
            progress_bar.update(1)

    return cards_prepared_to_json


@check_time
def run(url_site):
    """Main controller function"""
    headers = change_user_agent()
    full_url_domain_name = get_full_url_domain_name(url_site)

    card_link = get_link_to_card(headers, full_url_domain_name, url_site)

    cards_prepared_to_json = prepare_card_details(headers, full_url_domain_name, card_link)
    write_to_json(cards_prepared_to_json, PATH_TO_GOODS)

    print("\033[1m\033[32m<<-- Finished! -->>\033[0m")


if __name__ == '__main__':
    url_site = "https://scrapingclub.com/exercise/list_basic/?page="
    run(url_site)
