import os

import requests
from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm
from webdriver_manager.chrome import ChromeDriverManager

from must_have.crome_options import setting_chrome_options

logger.add("output.log", format="{time} {level} {message}", level="INFO")


def get_preview_mail_report(photos_report: dict, report_date: str):
    picture_folder = f'{"/Users/evgeniy/Library/Mobile Documents/com~apple~CloudDocs/TASS/"}{report_date}'
    os.makedirs(picture_folder, exist_ok=True)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=setting_chrome_options())

    count = 1

    for photo_id, income in tqdm(photos_report.items()):

        for money in income:
            rounded_money = f"{money:.2f}"

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
                get_image = requests.get(picture)
                with open(f"{picture_folder}/{photo_id}_{rounded_money}-({count}).jpg", 'wb') as img_file:
                    img_file.write(get_image.content)
                count += 1
            except Exception as NoSuchElementException:
                logger.info(f"image {photo_id = } don't found")

    driver.close()
    driver.quit()


if __name__ == '__main__':
    photos = {1439890: [327.888324873], 45600520: [172.551020408], 53596363: [275.65, 345.692913385]}
    get_preview_mail_report(photos, 'month and year')
