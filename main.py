import requests
from bs4_tutorial import download_txt
from bs4 import BeautifulSoup
from bs4_tutorial import check_for_redirect


def main():
    book_url = "https://tululu.org/txt.php"
    book_start_url = 'https://tululu.org/b'

    for count in range(10):
        params = {'id': count + 1}
        url = book_start_url + str(count + 1) + '/'
        response = requests.get(url)
        response.raise_for_status()

        try:
            check_for_redirect(response)
            soup = BeautifulSoup(response.text, 'lxml')
            title_tag = soup.find('h1')
            filename = title_tag.text.split('::')[0].strip()

            download_txt(book_url, filename, params=params)

        except requests.TooManyRedirects:
            continue


if __name__ == '__main__':
    main()
