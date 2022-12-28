import requests
from bs4 import BeautifulSoup
from functions import parse_book_page, check_for_redirect
from urllib.parse import urljoin

base_url = 'https://tululu.org'
url_with_fantasy = 'https://tululu.org/l55/'

response = requests.get(url_with_fantasy)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'lxml')

second_part_of_url = soup.find(class_='d_book').find('a')['href']

url_with_first_book = urljoin(base_url, second_part_of_url)

print(url_with_first_book)

