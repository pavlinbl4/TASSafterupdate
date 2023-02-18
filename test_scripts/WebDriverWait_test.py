"""
проверяю ка работает селениум и устанавливаю умную задержку на открытие сайта
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from must_have.crome_options import setting_chrome_options


def main(html):
    soup = BeautifulSoup(html, 'lxml')
    thumbs_data = soup.find('ul', id="mosaic").find_all('div', class_="thumb-content thumb-width thumb-height")
    images_on_page = len(soup.find('ul', id="mosaic").find_all('a', class_="zoom"))
    for i in range(images_on_page):
        image_date = thumbs_data[i].find(class_="date").text
        image_id = thumbs_data[i].find(class_="title").text
        image_title = thumbs_data[i].find('p').text
        image_caption = soup.find('ul', id="mosaic").find_all(class_="thumb-text")[i].text.strip().split('\n')[
            -1].lstrip().replace(
            ' Семен Лиходеев/ТАСС', '')
        image_link = soup.find('ul', id="mosaic").find_all('a', class_="zoom")[i].find('img').get('src')
        print(image_id, image_date)
        print(image_title)
        print(image_caption)
        print(image_link)


def get_html():
    options = setting_chrome_options()
    browser = webdriver.Chrome(options=options)

    browser.get('https://www.tassphoto.com/ru')
    WebDriverWait(browser, 10).until(
        ec.presence_of_element_located((By.ID, "userrequest"))
    )
    search_input = browser.find_element(By.ID, "userrequest")
    search_input.clear()
    search_input.send_keys('Семен Лиходеев')
    search_input.send_keys(Keys.ENTER)
    html = browser.page_source

    browser.close()
    browser.quit()

    return html


if __name__ == '__main__':
    main(get_html())
