import requests
from bs4 import BeautifulSoup
from functions import parse_book_page, check_for_redirect
from urllib.parse import urljoin

def get_url_with_book(soup):
    urls_with_books = soup.find_all(class_='d_book')
    for url in urls_with_books:
        second_part_of_url = url.find('a')['href']
        url_with_book = urljoin(base_url, second_part_of_url)
        print(url_with_book)

base_url = 'https://tululu.org'
url_with_fantasy = 'https://tululu.org/l55/'

response = requests.get(url_with_fantasy)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'lxml')

# second_part_of_url = soup.find(class_='d_book').find('a')['href']

# url_with_first_book = urljoin(base_url, second_part_of_url)

count = 10
for page in range(1, count):
    url_to_each_page = urljoin(url_with_fantasy, str(page))
    response = requests.get(url_to_each_page)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    get_url_with_book(soup)