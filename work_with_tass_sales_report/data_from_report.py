import re
from loguru import logger


def get_info_from_report(mail_report: dict, file_extension: str) -> dict:
    # словарь, где ключ - id снимка, а значение список с цифрами покупок
    photos = {}
    for i in mail_report:
        # logger.info(mail_report[i][0])
        if re.search(r'\d', str(mail_report[i][0])):
            money, photo_id = extract_money_value_from_mail_report(file_extension, i, mail_report)
            photos.setdefault(photo_id, [])
            photos[photo_id].append(money)
    return photos


def extract_money_value_from_mail_report(file_extension, i, mail_report):
    photo_id = mail_report[i][3]
    logger.info(f"{photo_id = }")
    remove_spaces_and_comma_in_mail_report = None
    if file_extension == '.xlsx':
        logger.info(f"File report is XLSX - {type(mail_report[i][5])}")
        if isinstance(mail_report[i][5], (int, float)):
            logger.info(
                f"Old type report {mail_report[i][5] = }, {type(mail_report[i][5])}")  # for old xlsx report - money in 5 column
            remove_spaces_and_comma_in_mail_report = mail_report[i][5]  # for old report money is integer
        elif isinstance(mail_report[i][5], str):
            logger.info(f" New type report {mail_report[i][6] = }")
            remove_spaces_and_comma_in_mail_report = mail_report[i][6].replace(' ', '').replace(',', '.')

    elif file_extension == '.html':
        remove_spaces_and_comma_in_mail_report = mail_report[i][5].replace(' ', '').replace(',', '.')

    money = float(remove_spaces_and_comma_in_mail_report)
    return money, photo_id
