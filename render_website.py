import json
import os
import pathlib

from more_itertools import chunked

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)


def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


json_path = find('books.json', pathlib.Path.cwd())

with open(json_path, 'r', encoding='utf-8') as file:
    books_descriptions = json.load(file)

book_cards_per_page = 10
book_cards_in_column = 2
books_on_page = list(chunked(books_descriptions, book_cards_per_page))

os.makedirs('pages', exist_ok=True)


def on_reload():
    for page, books in enumerate(books_on_page, start=1):
        books_for_columns = list(chunked(books, book_cards_in_column))
        page_title = f'index{page}.html'

        template = env.get_template('template.html')
        rendered_page = template.render(
            books=books_for_columns,
            total_pages=len(books_on_page),
            current_page=page,
        )

        with open(f'pages/{page_title}', 'w', encoding="utf8") as file:
            file.write(rendered_page)

    print('Site rebuilt')


# on_reload()
#
# server = Server()
# server.watch('template.html', on_reload)
# server.serve(root='.')
