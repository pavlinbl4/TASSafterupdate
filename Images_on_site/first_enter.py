from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from must_have.crome_options import setting_chrome_options
import time


def first_enter():
    browser = webdriver.Chrome(options=setting_chrome_options())

    browser.get('https://www.tassphoto.com/ru')
    WebDriverWait(browser, 10).until(
        ec.presence_of_element_located((By.ID, "userrequest"))
    )
    search_input = browser.find_element(By.ID, "userrequest")
    search_input.clear()
    search_input.send_keys('Семен Лиходеев')
    search_input.send_keys(Keys.ENTER)
    return browser


if __name__ == '__main__':
    start_page = first_enter()
    time.sleep(3)
    start_page.close()
    start_page.quit()
