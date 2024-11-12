import os

from loguru import logger
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from tqdm import tqdm
from webdriver_manager.chrome import ChromeDriverManager

from download_tass_preview import download_photo_preview_by_id
from must_have.crome_options import setting_chrome_options
from work_with_tass_sales_report.pars_tass_mail import get_year_from_report_date

logger.add("output.log", format="{time} {level} {message}", level="INFO")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=setting_chrome_options())


def get_preview_mail_report(photos_report: dict, report_date: str):
    year: str = get_year_from_report_date(report_date)

    try:
        picture_folder_downloads = f'{"/Users/evgeniy/Library/Mobile Documents/com~apple~CloudDocs/TASS/"}{year}/{report_date}'
        os.makedirs(picture_folder_downloads, exist_ok=True)
        logger.info(f"Images subfolder - {year}/{report_date}")

        count = 1

        for photo_id, incomes in tqdm(photos_report.items()):
            for income in incomes:
                rounded_money = f"{income:.2f}"
                image_file_name = f"{photo_id}_{rounded_money}-({count}).jpg"

                try:
                    download_photo_preview_by_id(photo_id,  picture_folder_downloads, image_file_name)

                    count += 1

                except NoSuchElementException as e:
                    logger.info(f"Image not found for photo_id: {photo_id} | Error: {e}")
                except Exception as e:
                    logger.error(f"An error occurred while processing photo_id {photo_id}: {str(e)}")
    finally:
        driver.quit()
