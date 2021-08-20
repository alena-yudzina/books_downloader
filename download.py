from os import name
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urlparse, urlsplit, urljoin, unquote
import argparse
import datetime


def parse_cli_args():
    parser = argparse.ArgumentParser(description='Download books')
    parser.add_argument('start_id', help='set start book id', type=int)
    parser.add_argument('end_id', help='set end book id', type=int)
    args = parser.parse_args()

    return args


def parse_book_page(page):
    soup = BeautifulSoup(page, 'lxml')
    title_and_author = soup.find('h1').text
    title, author = title_and_author.split('::')
    genres = soup.find('span', class_='d_book').find_all('a')
    genres = [genre.text for genre in genres]
    img_url = soup.find(class_='bookimage').find('img')['src']
    comments = soup.find_all('div', class_='texts')
    comments = [comment.find('span', class_='black').text for comment in comments]
    book_info = {
        'title': title.strip(),
        'author': author.strip(),
        'genre': genres,
        'img_url': img_url,
        'comments': comments
    }
    return book_info


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def download_txt(url, payload, filename, folder='books/'):

    response = requests.get(url, params=payload)
    check_for_redirect(response)
    response.raise_for_status()
    Path(folder).mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now().strftime('%y%m%d_%H%M%S')
    filename = '{}_{}.txt'.format(timestamp, sanitize_filename(filename))
    filepath = Path(folder) / filename
    with open(filepath, 'wb') as file:
        file.write(response.content)

    return filepath


def download_image(url, folder='images'):

    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    Path(folder).mkdir(parents=True, exist_ok=True)
    url_path = urlsplit(url).path
    filename = unquote(Path(url_path).name)
    timestamp = datetime.datetime.now().strftime('%y%m%d_%H%M%S')
    filename = '{}_{}'.format(timestamp, sanitize_filename(filename))
    filepath = Path(folder) / filename
    with open(filepath, 'wb') as file:
        file.write(response.content)

    return filepath


def main():
    args = parse_cli_args()
    for book_id in range(args.start_id, args.end_id + 1):
        url = 'https://tululu.org/b{}/'.format(book_id)
        response = requests.get(url)
        try:
            check_for_redirect(response)
            response.raise_for_status()
        except requests.HTTPError:
            continue

        book_info = parse_book_page(response.text)
        print('Заголовок:', book_info['title'])
        print('Автор:', book_info['author'])
        print()

        img_url = urljoin(url, book_info['img_url'])
        book_url = 'https://tululu.org/txt.php'
        payload = {'id': book_id}
        try:
            download_image(img_url)
            download_txt(book_url, payload, filename=book_info['title'])
        except requests.HTTPError:
            print('Unable to download book')


if __name__ == '__main__':
    main()
