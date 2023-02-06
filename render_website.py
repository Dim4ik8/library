import json
import os
import pathlib

from more_itertools import chunked

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server


def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


def on_reload(books_on_page, env):
    for page, books in enumerate(books_on_page, start=1):
        page_title = f'index{page}.html'

        template = env.get_template('template.html')
        rendered_page = template.render(
            books_catalog=books,
            total_pages=len(books_on_page),
            current_page=page,
        )
        with open(f'pages/{page_title}', 'w', encoding='utf8') as file:
            file.write(rendered_page)


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    json_path = find('books.json', pathlib.Path.cwd())

    with open(json_path, 'r', encoding='utf-8') as file:
        books_descriptions = json.load(file)

    book_cards_per_page = 10
    books_on_page = list(chunked(books_descriptions, book_cards_per_page))

    on_reload(books_on_page, env)

    server = Server()
    server.watch('template.html', on_reload(books_on_page, env))
    server.serve(root='.')


if __name__ == '__main__':
    main()
