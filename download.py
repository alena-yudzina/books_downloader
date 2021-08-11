from os import name
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urlparse, urlsplit, urljoin
import argparse


def parse_cli_args():
    parser = argparse.ArgumentParser(description='Download books')
    parser.add_argument('start_id', help='set start book id', type=int)
    parser.add_argument('end_id', help='set end book id', type=int)
    args = parser.parse_args()

    return args


def parse_book_page(page):
    book_info = {}
    soup = BeautifulSoup(page, 'lxml')
    title_and_author = soup.find('h1').text
    book_info['title'] = title_and_author.split('::')[0].strip()
    book_info['author'] = title_and_author.split('::')[1].strip()

    genres = soup.find('span', class_='d_book').find_all('a')
    genres_list = []
    for genre in genres:
        genres_list.append(genre.text)
    book_info['genre'] = genres_list

    img_url = soup.find(class_='bookimage').find('img')['src']
    book_info['img_url'] = img_url

    comments = soup.find_all('div', class_='texts')
    comments_list = []
    for comment in comments:
        comment_text = comment.find('span', class_='black').text
        comments_list.append(comment_text)
    book_info['comments'] = comments_list

    return book_info


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def download_txt(url, filename, folder='books/'):

    response = requests.get(url)
    try:
        check_for_redirect(response)
    except requests.HTTPError:
        return
    response.raise_for_status()
    Path(folder).mkdir(parents=True, exist_ok=True)
    filename = '{}.txt'.format(sanitize_filename(filename))
    with open(Path(folder) / filename, 'wb') as file:
        file.write(response.content)
    filepath = Path(folder) / filename
    
    return filepath


def download_image(url, folder='images'):

    response = requests.get(url)
    try:
        check_for_redirect(response)
    except requests.HTTPError:
        return
    response.raise_for_status()
    Path(folder).mkdir(parents=True, exist_ok=True)
    url_path = urlparse(url).path
    filename = url_path.rsplit('/', 1)[-1]
    filename = sanitize_filename(filename)
    with open(Path(folder) / filename, 'wb') as file:
        file.write(response.content)
    filepath = Path(folder) / filename
    
    return filepath

args = parse_cli_args()
for i in range(args.start_id, args.end_id + 1):
    url = 'https://tululu.org/b{}/'.format(i)
    response = requests.get(url)
    try:
        check_for_redirect(response)
    except requests.HTTPError:
        continue
    response.raise_for_status()

    book_info = parse_book_page(response.text)
    print('Заголовок:', book_info['title'])
    print('Автор:', book_info['author'])
    print()

    img_url = urljoin(url, book_info['img_url'])
    download_image(img_url)
    url = 'https://tululu.org/txt.php?id={}'.format(i)
    download_txt(url, filename=book_info['title'])
