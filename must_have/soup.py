from bs4 import BeautifulSoup
import requests


def get_soup(html):
    return BeautifulSoup(html, 'lxml')


def browser_response(url):
    response = requests.get(url)
    if response.ok:
        return response.text


def get_html(link, browser):
    browser.get(link)
    html = browser.page_source
    return html


if __name__ == '__main__':
    browser_response(
        'https://www.tassphoto.com/ru/asset/fullTextSearch/search/%D0%B2%D0%B0%D0%BB%D0%B5%D0%BD%D1%82%D0%B8%D0%BD%20%D0%90%D0%BD%D1%82%D0%BE%D0%BD%D0%BE%D0%B2/page/1')
