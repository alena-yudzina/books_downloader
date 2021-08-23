# Парсер книг с сайта tululu.org

Проект предназначен для скачивания книг с сайта [tululu.org].

### Как установить

```
pip3 install -r requirements.txt
```

### Аргументы

Программу можно использовать двумя способами:

1. Скачивание книг по id.

Программе необходимо передавать 2 аргумента: `start_page_id` и `end_page_id`.
```
python3 download.py 10 20
```

2. Скачивание книг по страницам из категории научная фантастика.

Программе можно передавать следующие аргументы:

`start_page`, `end_page`, `dest_folder`, `dest_folder`, `skip_txt`, `skip_imgs`, `json_path`.
```
python3 parse_tululu_category.py --start_page 5 --end_page 10 --skip_txt --json_path /Users/Harry/downloads
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).