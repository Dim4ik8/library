# Парсер книг с сайта электронной бибилиотеки
Скрипт помогает скачивать книги с сайта электронной библиотеки [tululu.org](https://tululu.org/).

## Как установить
Для запуска скриптов необходим Python 3 и выше версии.
Чтобы парсер работал корректно необходимо установить виртуальное окружение:
```python
python -m venv venv

```
и активировать его командами:
- для Windows:
```python
./venv/Scripts/activate.ps1
```
- для Linux:
```python
source venv/bin/activate
```
Далее важно установить зависимости (необходимые для работы скрипта бибилиотеки):
```python
pip install -r requirements.txt
```
Запуск первого скрипта осуществляется командой:
```python
python parse_tululu.py
```
Запуск второго происходит через команду:
```python
python parse_tululu_category.py
```
Разница между скриптами состоит в том, что `parse_tululu.py` имеет меньше аргументов командной строки и не сохраняет файл JSON с информацией о скачанных книгах.
## Подробнее об аргументах 
По умолчанию первый парсер качает книги с 1-ой по 10-ую, второй - с 1-ой по 701-ую. Чтобы задать свои условия по количеству и порядку скачиваемых книг, для обоих скриптов существуют аргументы `-s` и `-e`, обозначающие начальную и конечную книгу для скачивания.
Примеры вызова скриптов с аргументами (будут скачаны книги с 10й по 30ую):
```python
parse_tululu.py -s 10 -e 30
python parse_tululu_category.py -s 10 -e 30
```
Далее речь пойдет об описании аргументов только скрипта `parse_tululu_category.py`
у него имеется аргумент для передачи названия директории, в которую будут сохранятся книги `-d`. Пример вызова парсера с аргументами (будут скачаны книги с 1 по 25 страницу и помещены в папку Fantasy):
```python
python parse_tululu_category.py -s 1 -e 25 -dFantasy
```
Также имеются особенные аргументы, отвечающие за скачивание картинок и текстов книг. `skip_imgs` и `skip_text` соответственно. Пример вызова парсера с аргументами (в папку Best будут скачаны книги с 10 по 403 страницу но без текстов и картинок):
```python
python parse_tululu_category.py -s 10 -e 403 -dBest --skip_imgs --skip_text
```
Последний аргумент позволяет указать папку для сохранения JSON файла с информацией о скачанных книгах. `-j`. Пример вызова парсера с аргументами (будут скачаны книги с картинками и текстами с 4 по 100 страницы в папку Night, а JSON файл будет помещен отдельно в папку Info): 
```python
python parse_tululu_category.py -s 4 -e 100 -dBest -jInfo
```
Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).