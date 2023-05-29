from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from must_have.crome_options import setting_chrome_options
import time

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



if __name__ == '__main__':
    first_enter()
    time.sleep(10)
    browser.close()
    browser.quit()