from bs4 import BeautifulSoup
from selenium import webdriver
from must_have.crome_options import setting_chrome_options


def get_soup(html):
    return BeautifulSoup(html, 'lxml')

def get_html(link):
    browser = webdriver.Chrome(options=setting_chrome_options())
    browser.get(link)
    html = browser.page_source
    return html
