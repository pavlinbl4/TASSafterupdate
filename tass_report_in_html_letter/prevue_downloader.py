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
from loguru import logger


def get_preview_mail_report(photos_report: dict, report_date: str):
    picture_folder = f'{"/Users/evgeniy/Library/Mobile Documents/com~apple~CloudDocs/TASS/"}{report_date}'
    os.makedirs(picture_folder, exist_ok=True)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=setting_chrome_options())

    count = 1

    for photo_id, income in tqdm(photos_report.items()):

        for money in income:
            rounded_money = f"{money:.2f}"
            logger.info(f"{count} {photo_id = }, {rounded_money = }")

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
                logger.info(NoSuchElementException)
                logger.info(f"image {photo_id = } don't found")

    driver.close()
    driver.quit()


if __name__ == '__main__':
    photos = {1439890: [327.888324873], 45600520: [172.551020408], 53596363: [275.65, 345.692913385]}
    get_preview_mail_report(photos, 'month and year')
