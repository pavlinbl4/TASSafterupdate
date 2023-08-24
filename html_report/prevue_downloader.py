import os
from selenium import webdriver
import requests
from selenium.webdriver.common.by import By
from must_have.crome_options import setting_chrome_options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import re


def get_preview_mail_report(mail_report: dict, report_date: str):
    picture_folder = f'{"/Users/evgeniy/Library/Mobile Documents/com~apple~CloudDocs/TASS/"}{report_date}'
    os.makedirs(picture_folder, exist_ok=True)
    browser = webdriver.Chrome(options=setting_chrome_options())
    for i in mail_report:
        if re.search(r'\d', mail_report[i][0]):
            print(mail_report[i])
            photo_id = mail_report[i][3]
            money = float(mail_report[i][5].replace(',', '.'))
            try:
                browser.get('https://www.tassphoto.com/ru')
                WebDriverWait(browser, 10).until(
                    ec.presence_of_element_located((By.ID, "userrequest"))
                )
                browser.get(f'https://www.tassphoto.com/ru/asset/fullTextSearch/search/{photo_id}/page/1')
                WebDriverWait(browser, 10).until(
                    ec.presence_of_element_located((By.ID, "userrequest"))
                )

                picture = browser.find_element(By.CSS_SELECTOR, f"img.thumb{photo_id}").get_attribute("src")
                print(picture)
                get_image = requests.get(picture)
                with open(f"{picture_folder}/{photo_id}_{money}.jpg", 'wb') as img_file:
                    img_file.write(get_image.content)
            except Exception as ex:
                print(ex)
                browser.close()
                browser.quit()
    browser.close()
    browser.quit()
