from bs4 import BeautifulSoup


def get_soup(html):
    return BeautifulSoup(html, 'lxml')


def get_html(link, browser):
    browser.get(link)
    html = browser.page_source
    return html
