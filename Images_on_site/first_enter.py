import time
from loguru import logger

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from browser.check_selenium import open_page_with_selenium


def first_enter(search_word):

    driver = open_page_with_selenium('https://www.tassphoto.com/ru')

    # enter word in search field
    WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.ID, "userrequest"))
    )
    search_input = driver.find_element(By.ID, "userrequest")
    search_input.clear()
    search_input.send_keys(search_word)
    search_input.send_keys(Keys.ENTER)
    logger.debug(driver.current_url)
    return driver


if __name__ == '__main__':
    start_page = first_enter('Семен Лиходеев')
    time.sleep(3)
    print(start_page.title)
    start_page.close()
    start_page.quit()
