import json
import os
import pathlib

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

with open(json_path, 'r') as file:
    books = json.load(file)

def on_reload():
    template = env.get_template('template.html')
    rendered_page = template.render(
        books=books,
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    print("Site rebuilt")

on_reload()

server = Server()

server.watch('template.html', on_reload)

server.serve(root='.')


