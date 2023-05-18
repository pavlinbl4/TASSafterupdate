from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys

from Images_on_site.count_images import get_page_numbers
from must_have.crome_options import setting_chrome_options
from must_have.make_documents_subfolder import make_documents_subfolder
from must_have.soup import get_soup, get_html

browser = webdriver.Chrome(options=setting_chrome_options())


def first_enter():
    browser.get('https://www.tassphoto.com/ru')
    WebDriverWait(browser, 10).until(
        ec.presence_of_element_located((By.ID, "userrequest"))
    )
    search_input = browser.find_element(By.ID, "userrequest")
    search_input.clear()
    search_input.send_keys('Семен Лиходеев')
    search_input.send_keys(Keys.ENTER)


def check_all_images():  # 1. start to check images
    url = 'https://www.tassphoto.com/ru/asset/fullTextSearch/search/' \
          '%D0%A1%D0%B5%D0%BC%D0%B5%D0%BD%20%D0%9B%D0%B8%D1%85%D0%BE%D0%B4%D0%B5%D0%B5%D0%B2/page/'

    page_number, images_online = get_page_numbers(url)  # 2. get number of images on site
    from xlsx_tools.create_all_TASS_images import create_xlsx
    ws, wb = create_xlsx(report_folder)
    count = 1
    for n in range(1, page_number + 1):  # количество страниц  на сайте для анализа  - page_number + 1
        link = f'{url}{n}'
        soup = get_soup(get_html(link))
        thumbs_data = soup.find('ul', id="mosaic").find_all('div', class_="thumb-content thumb-width thumb-height")
        images_on_page = len(soup.find('ul', id="mosaic").find_all('a', class_="zoom"))
        for i in range(images_on_page):
            count += 1
            image_date = thumbs_data[i].find(class_="date").text
            image_id = thumbs_data[i].find(class_="title").text
            image_title = thumbs_data[i].find('p').text
            if soup.find('ul', id="mosaic") is not None:
                image_caption = soup.find('ul', id="mosaic").find_all(class_="thumb-text")[i].text.strip().split('\n')[
                    -1].lstrip().replace(' Семен Лиходеев/ТАСС', '').replace(' Фото ИТАР-ТАСС/ Семен Лиходеев', '')
            else:
                image_caption = "Some problem with caption"
            image_link = soup.find('ul', id="mosaic").find_all('a', class_="zoom")[i].find('img').get('src')
            print(count - 1, image_id, image_date)
            print(image_title)
            print(image_caption)
            print(image_link)
            ws[f'A{count}'] = images_online + 1 - count
            ws[f'B{count}'] = image_id
            ws[f'C{count}'] = image_date
            ws[f'D{count}'] = image_caption
            ws[f'E{count}'] = image_link
    wb.save(f'{report_folder}/all_TASS_images.xlsx')
    wb.close()


if __name__ == '__main__':
    report_folder = make_documents_subfolder('TASS/Tass_data')
    first_enter()
    check_all_images()
    browser.close()
    browser.quit()
