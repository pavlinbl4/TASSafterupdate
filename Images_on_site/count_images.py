from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from must_have.crome_options import setting_chrome_options
from must_have.soup import get_soup, get_html, browser_response


def get_image_numbers_with_selenium(url):  # get number of images on site
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=setting_chrome_options())
    soup = get_soup(get_html(url, driver))
    driver.close()
    driver.quit()

    images_online = soup.find('p', id='nb-result').get_text()
    return images_online


def get_image_numbers_with_soup(url):
    soup = get_soup(browser_response(url))
    images_online = soup.find('p', id='nb-result').text
    return images_online


if __name__ == '__main__':
    url_tass = 'https://www.tassphoto.com/ru/asset/fullTextSearch/search/Валентин+Антонов/page/1'

    encoded_url = quote(url_tass, safe=':/')
    print(get_image_numbers_with_soup(encoded_url))
