from must_have.crome_options import setting_chrome_options
from must_have.soup import get_soup, get_html
from selenium import webdriver


def get_page_numbers(url, browser):  # get number of images on site
    soup = get_soup(get_html(url, browser))
    images_online = int(str(soup.select(".result-counter#nb-result"))[42:47])
    page_number = images_online // 20 + 1
    return page_number, images_online


if __name__ == '__main__':
    url_tass = 'https://shorturl.at/dCKLR'
    browser = webdriver.Chrome(options=setting_chrome_options())
    print(get_page_numbers(url_tass, browser))
    browser.close()
    browser.quit()




