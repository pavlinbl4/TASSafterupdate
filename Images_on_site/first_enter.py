import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from must_have.crome_options import setting_chrome_options


def first_enter(search_word):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=setting_chrome_options())

    driver.get('https://www.tassphoto.com/ru')


    WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.ID, "userrequest"))
    )
    search_input = driver.find_element(By.ID, "userrequest")
    search_input.clear()
    search_input.send_keys(search_word)
    search_input.send_keys(Keys.ENTER)
    return driver


if __name__ == '__main__':
    start_page = first_enter('Семен Лиходеев')
    time.sleep(3)
    print(start_page.title)
    start_page.close()
    start_page.quit()
