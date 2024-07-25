import os
from selenium import webdriver
import requests
from selenium.webdriver.common.by import By
from must_have.crome_options import setting_chrome_options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import re
from tqdm import tqdm
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from work_with_tass_sales_report.data_from_report import extract_money_value_from_report_file


def get_preview_mail_report(mail_report: dict, report_date: str, file_extension:str):
    picture_folder = f'{"/Users/evgeniy/Library/Mobile Documents/com~apple~CloudDocs/TASS/"}{report_date}'
    os.makedirs(picture_folder, exist_ok=True)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=setting_chrome_options())

    for i in tqdm(mail_report):
        if re.search(r'\d', mail_report[i][0]):
            money, photo_id = extract_money_value_from_report_file(file_extension, i, mail_report)
            try:
                driver.get('https://www.tassphoto.com/ru')
                WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located((By.ID, "userrequest"))
                )
                driver.get(f'https://www.tassphoto.com/ru/asset/fullTextSearch/search/{photo_id}/page/1')
                WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located((By.ID, "userrequest"))
                )

                picture = driver.find_element(By.CSS_SELECTOR, f"img.thumb{photo_id}").get_attribute("src")
                # print(f'{picture = }')
                get_image = requests.get(picture)
                with open(f"{picture_folder}/{photo_id}_{money}-({mail_report[i][0]}).jpg", 'wb') as img_file:
                    img_file.write(get_image.content)
            except Exception as ex:
                print(ex)
                driver.close()
                driver.quit()
    driver.close()
    driver.quit()
