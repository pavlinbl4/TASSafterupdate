from bs4 import BeautifulSoup


def get_soup(html):
    return BeautifulSoup(html, 'lxml')
