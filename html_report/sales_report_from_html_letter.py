from tkinter import filedialog
from html_report.pars_tass_mail import report_from_tass_mail, get_report_date
from html_report.prevue_downloader import get_preview_mail_report
from html_report.write_to_xlsx import write_to_main_file
import re

main_report = '/Users/evgeniy/Library/Mobile Documents/com~apple~CloudDocs/TASS/all_years_report.xlsx'
mail_as_html = filedialog.askopenfile().name


def get_info_from_report(mail_report: dict) -> dict:
    photos = {}
    for i in mail_report:
        if re.search(r'\d', mail_report[i][0]):
            print(mail_report[i])
            photo_id = mail_report[i][3]
            money = float(mail_report[i][5].replace(',', '.'))
            photos.setdefault(photo_id, [])
            photos[photo_id].append(money)
    return photos  # словарь где ключ  id снимка , а значение список с цифрами покупок


def tass_sales():
    mail_report = report_from_tass_mail(mail_as_html)
    report_date = get_report_date(mail_report)
    print(f"{report_date = }")
    photos = get_info_from_report(mail_report)
    write_to_main_file(photos, main_report, report_date)
    get_preview_mail_report(mail_report, report_date)


if __name__ == '__main__':
    tass_sales()
