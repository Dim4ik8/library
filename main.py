import requests
from pathlib import Path


def main():
    book_url = "https://tululu.org/txt.php"

    Path("books").mkdir(parents=True, exist_ok=True)

    for count in range(10):
        params = {'id': count + 1}
        response = requests.get(book_url, params=params)
        response.raise_for_status()
        filename = Path.cwd() / 'books' / f'id{count+1}.txt'
        with open(filename, 'w', encoding='UTF-8') as file:
            file.write(response.text)


if __name__ == '__main__':
    main()
