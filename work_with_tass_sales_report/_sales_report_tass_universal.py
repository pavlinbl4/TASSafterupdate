"""
Главный модуль программы для обработки отчета от ТАСС.
Вносит данные о продаже в единый файл и скачивает превью купленных снимков
"""
import os
import re
from pathlib import Path
from tkinter import filedialog

import openpyxl
import requests
from bs4 import BeautifulSoup
from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm
from webdriver_manager.chrome import ChromeDriverManager

from must_have.crome_options import setting_chrome_options
from xlsx_tools.write_to_xlsx import write_to_main_file

main_report = '/Users/evgeniy/Library/Mobile Documents/com~apple~CloudDocs/TASS/all_years_report.xlsx'


def get_preview_mail_report(mail_report: dict, report_date: str, file_extension: str):
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


# create dict from xlsx file, index row number, value - list from columns date
def report_from_tass_xlsx_file(xlsx_file: str) -> dict:
    wb = openpyxl.load_workbook(xlsx_file)
    sheet = wb.active
    report = {}
    for number, value in enumerate(sheet.rows, start=1):
        report[number] = [cell.value if cell.value is not None else '' for cell in sheet[number]]
    return report


def get_info_from_report(mail_report: dict, file_extension: str) -> dict:
    # словарь, где ключ - id снимка, а значение список с цифрами покупок
    photos = {}
    for i in mail_report:
        logger.info(mail_report[i][0])
        if re.search(r'\d', mail_report[i][0]):
            money, photo_id = extract_money_value_from_report_file(file_extension, i, mail_report)
            logger.info(f'{money = }')
            photos.setdefault(photo_id, [])
            photos[photo_id].append(money)
    return photos


def extract_money_value_from_report_file(file_extension, i, mail_report):
    photo_id = mail_report[i][3]
    column_number = 5  # for html report
    if file_extension == '.xlsx':
        column_number = 6
    remove_spaces_and_comma_in_mail_report = mail_report[i][column_number].replace(' ', '').replace(',', '.')
    money = float(remove_spaces_and_comma_in_mail_report)
    return money, photo_id


# from html report file extract dict with information about sales,
# index row number, value - list from columns date
def report_from_html_report_file(path_to_report_file: str) -> dict:
    with open(path_to_report_file, 'r') as report_file:
        table = BeautifulSoup(report_file, 'lxml')
    table = table.find('tbody')
    table = table.find_all('tr')[4:]  # start with data row in table
    row_in_table = [x for x in table]
    report = {}
    for i in range(len(table)):
        report[i] = [x.text.strip() for x in row_in_table[i].find_all('td')]
    return report


def get_report_date(mail_report, file_extension):
    if file_extension == '.html':
        logger.info(mail_report[0][2])
        return mail_report[0][2]
    elif file_extension == '.xlsx':
        logger.info(mail_report[6][2])
        return mail_report[6][2]


def tass_sales():
    path_to_report_file = filedialog.askopenfile().name
    logger.info(path_to_report_file)

    # check file extension
    file_extension = Path(path_to_report_file).suffix
    logger.info(file_extension)

    mail_report = extract_mail_report(file_extension, path_to_report_file)
    # mail_report -  dict with index row number, value - list from columns date
    logger.info(mail_report)

    # get date - year and month from mail_report
    report_date = get_report_date(mail_report, file_extension)
    logger.info(report_date)

    # create dict with images id and sales information
    photos = get_info_from_report(mail_report, file_extension)
    # photos dict with index photo id and  list with money income
    logger.info(photos)

    write_to_main_file(photos, main_report, report_date)
    get_preview_mail_report(mail_report, report_date, file_extension)


# check file extension and extract data from suitable file
def extract_mail_report(file_extension, path_to_report_file):
    mail_report = None
    if file_extension == '.html':
        # for the html report
        mail_report = report_from_html_report_file(path_to_report_file)
    elif file_extension == '.xlsx':
        # for the xlsx report
        mail_report = report_from_tass_xlsx_file(path_to_report_file)
    else:
        print("wrong report file type")
    # index row number, value - list from columns date
    return mail_report


if __name__ == '__main__':
    tass_sales()
