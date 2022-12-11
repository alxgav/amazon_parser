import csv
import os
from datetime import datetime
from time import time

import httpx
from loguru import logger
from selectolax.parser import HTMLParser

from models import Book

''' ** config ** '''
start_time = time()
path = os.path.dirname(os.path.realpath(__file__))
logger.add(f'log/log.log', 
           format= '{time} {level} {message}', 
           level='DEBUG', 
           serialize=False, 
           rotation='1 month', 
           compression='zip')
logger.info(f'Start app {datetime.today()}')




headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
           'accept': 'text/html, */*; q=0.01',
           'authority': 'www.amazon.com',
           'method': 'GET',
           'schemel': 'https'}

home_url = 'https://www.amazon.com'
url = 'https://www.amazon.com/best-sellers-books-Amazon/zgbs/books/16273/ref=zg_bs_pg_1?_encoding=UTF8&pg=1'


def get_html(page:int)-> HTMLParser:
    url = f'https://www.amazon.com/best-sellers-books-Amazon/zgbs/books/16273/ref=zg_bs_pg_{page}?_encoding=UTF8&pg={page}'
    print(url)
    response = httpx.get(url, headers=headers)
    return HTMLParser(response.text)

def amazon_data(html: HTMLParser) -> Book:

    books = []
    for item in html.css('div.p13n-sc-uncoverable-faceout'):
        title = item.css_first('a.a-link-normal span').text()
        try:
            author = item.css_first('a.a-size-small.a-link-child div').text()
        except:
            author = ''
        try:
            url_book = f"{home_url}{item.css_first('a.a-link-normal').attributes['href']}"
            
        except:
            url_book = home_url
        try:
            rating = float(item.css_first('a.a-link-normal span.a-icon-alt').text().split()[0].strip())
        except:
            rating = 0.0
        price = item.css_first('a.a-link-normal.a-text-normal span.a-size-base.a-color-price').text().split()[0]
        
        book_data = Book(title= title,
                        author= author,
                        rating=rating,
                        type_of_book=item.css_first('div.a-row.a-size-small span.a-size-small.a-color-secondary.a-text-normal').text(),
                        price=price,
                        url=url_book).dict()
        books.append(book_data)
    return books

def books_to_csv(books: list):
    header = ['title', 'author', 'rating', 'type_of_book', 'price', 'url']
    with open('books.csv', 'a') as csv_file:
        writer = csv.DictWriter(csv_file, delimiter=';', fieldnames=header)
        if csv_file.tell() == 0:
            writer.writeheader()
        
        writer.writerows(books)



@logger.catch
def main():
    for page in range(1,3):
        books_to_csv(amazon_data(get_html(page)))

if __name__ =='__main__':
    main()
    logger.info("--- %s seconds ---" % (time() - start_time))
    logger.info(f'End app {datetime.today()}')