"""
Главный модуль программы для обработки отчета от ТАСС.
Вносит данные о продаже в единый файл и скачивает превью купленных снимков
"""

from pathlib import Path
from tkinter import filedialog

from loguru import logger

from work_with_tass_sales_report.data_from_report import get_info_from_report
from work_with_tass_sales_report.extract_dict_from_xlsx_report import report_from_tass_xlsx_file
from tass_report_in_html_letter.pars_tass_mail import report_from_tass_mail, get_report_date
from tass_report_in_html_letter.prevue_downloader import get_preview_mail_report
from tass_report_in_html_letter.write_to_xlsx import write_to_main_file

main_report = '/Users/evgeniy/Library/Mobile Documents/com~apple~CloudDocs/TASS/all_years_report.xlsx'


def tass_sales():
    path_to_report_file = filedialog.askopenfile().name
    logger.info(path_to_report_file)

    # check file extension
    file_extension = Path(path_to_report_file).suffix
    logger.info(file_extension)

    mail_report = extract_mail_report(file_extension, path_to_report_file)
    # mail_report -  dict with index row number, value - list from columns date
    logger.info(mail_report)

    # get date from report file
    report_date = get_report_date(mail_report, file_extension)
    logger.info(report_date)

    # create dict with images id and sales information
    photos = get_info_from_report(mail_report, file_extension)
    # photos dict with index photo id nad value list with money income
    logger.info(photos)

    write_to_main_file(photos, main_report, report_date)
    # get_preview_mail_report(mail_report, report_date, file_extension)
    # print(photos)


# check file extension and extract data from suitable file
def extract_mail_report(file_extension, path_to_report_file):
    mail_report = None
    if file_extension == '.html':
        # for the html report
        mail_report = report_from_tass_mail(path_to_report_file)
    elif file_extension == '.xlsx':
        # for the xlsx report
        mail_report = report_from_tass_xlsx_file(path_to_report_file)
    else:
        print("wrong report file type")
    # index row number, value - list from columns date
    return mail_report


if __name__ == '__main__':
    tass_sales()
