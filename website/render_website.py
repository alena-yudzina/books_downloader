import json
import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('website/template.html')

    with open("fantasy_books_info.json", "r") as file:
        books_info = file.read()
    books_info = json.loads(books_info)
    books_pages = list(chunked(books_info, 10))
    Path('website/pages').mkdir(parents=True, exist_ok=True)
    for page, books in enumerate(books_pages, start=1):
        books_rows = list(chunked(books, 2))
        rendered_page = template.render(books_rows=books_rows)
        with open('website/pages/index{}.html'.format(page), 'w', encoding="utf8") as file:
            file.write(rendered_page)


on_reload()
server = Server()
server.watch('website/template.html', on_reload)
server.serve(root='website/pages')
