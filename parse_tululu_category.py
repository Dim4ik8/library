import json

import requests
from bs4 import BeautifulSoup
import logging
import re
from functions import check_for_redirect, download_the_book
from urllib.parse import urljoin

logger = logging.getLogger()
def get_links_to_books(soup):
    books = soup.find_all(class_='d_book')
    links_to_books = [urljoin(base_url, url.find('a')['href']) for url in books]
    return links_to_books

base_url = 'https://tululu.org'
url_to_fantasy_books = 'https://tululu.org/l55/'
url_with_text = 'https://tululu.org/txt.php'

response = requests.get(url_to_fantasy_books)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'lxml')
second_part_of_url = soup.find(class_='d_book').find('a')['href']
url_to_first_book = urljoin(base_url, second_part_of_url)

count_of_pages = 4
books = []

for page in range(1, count_of_pages+1):
    url_to_each_page = urljoin(url_to_fantasy_books, str(page))
    response = requests.get(url_to_each_page)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    links_to_books = get_links_to_books(soup)
    for link in links_to_books:
        try:
            id = re.findall('\d+', link)[0]
            params = {'id': id}
            response = requests.get(link)
            response.raise_for_status()

            check_for_redirect(response)
            soup = BeautifulSoup(response.text, 'lxml')

            book = download_the_book(soup, link, url_with_text, params)

            books.append(book)

        except requests.TooManyRedirects:
            logger.warning(f'There is no data for one book ..')
            continue

        except requests.exceptions.HTTPError:
            logger.warning('Some errors on server.. Try again')
            continue

        except requests.exceptions.ConnectionError:

            logger.warning('Please check your internet connection')
            time.sleep(10)
with open('books.json', 'w') as file:
    json.dump(books, file, ensure_ascii=False)

with open('books.json', 'r') as file:
    all_books = json.load(file)

for count, book in enumerate(all_books):
    print(count+1, '---', book['title'])