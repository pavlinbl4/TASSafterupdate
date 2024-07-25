import re
from loguru import logger


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
