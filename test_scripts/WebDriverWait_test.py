"""
проверяю ка работает Selenium и устанавливаю умную задержку на открытие сайта
"""

from bs4 import BeautifulSoup

from Images_on_site.first_enter import first_enter


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
    browser = first_enter()

    html = browser.page_source

    browser.close()
    browser.quit()

    return html


if __name__ == '__main__':
    main(get_html())
