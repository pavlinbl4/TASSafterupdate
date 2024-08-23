import os
import requests
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from loguru import logger
from must_have.crome_options import setting_chrome_options

logger.add("output.log", format="{time} {level} {message}", level="INFO")


def get_preview_mail_report(photos_report: dict, report_date: str):
    picture_folder = f'{"/Users/evgeniy/Library/Mobile Documents/com~apple~CloudDocs/TASS/"}{report_date}'
    os.makedirs(picture_folder, exist_ok=True)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=setting_chrome_options())

    count = 1

    for photo_id, incomes in tqdm(photos_report.items()):
        for income in incomes:
            rounded_money = f"{income:.2f}"

            try:
                driver.get(f'https://www.tassphoto.com/ru/asset/fullTextSearch/search/{photo_id}/page/1')
                WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located((By.ID, "userrequest"))
                )

                picture_element = driver.find_element(By.CSS_SELECTOR, f"img.thumb{photo_id}")
                picture_url = picture_element.get_attribute("src")

                image_response = requests.get(picture_url)
                image_path = os.path.join(picture_folder, f"{photo_id}_{rounded_money}-({count}).jpg")

                with open(image_path, 'wb') as img_file:
                    img_file.write(image_response.content)

                count += 1
            except NoSuchElementException:
                logger.info(f"Image not found for photo_id: {photo_id}")
            except Exception as e:
                logger.error(f"An error occurred while processing photo_id {photo_id}: {str(e)}")

    driver.quit()
