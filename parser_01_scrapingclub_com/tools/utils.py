import json
import os
from urllib.parse import urljoin

from fake_useragent import UserAgent


def get_default_download_path(title):
    """Получение пути к папке "Downloads" в системе по умолчанию"""
    default_download_path = os.path.join(os.path.expanduser('~'), 'Downloads', title)
    return default_download_path


def change_user_agent():
    """Changes the user agent of the Chrome driver"""
    useragent = UserAgent()
    headers = {
        "User-Agent": useragent.google}
    return headers


def get_full_url_domain_name(url: str):
    """
    @before https://scrapingclub.com/exercise/list_basic/?
    @after https://scrapingclub.com/
    """
    return urljoin(url, '/')


def write_to_json(goods: list[dict[str, str]], json_file: str):
    with open(json_file, 'w') as file:
        json.dump(goods, file, indent=4)
