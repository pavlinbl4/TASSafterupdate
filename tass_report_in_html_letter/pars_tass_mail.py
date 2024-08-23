from bs4 import BeautifulSoup
from loguru import logger

from work_with_tass_sales_report.gui_select_file import select_file_via_gui


# from html report file extract dict with information about sales,
# index row number, value - list from columns date
def report_from_tass_mail(path_to_report_file: str) -> dict:
    try:
        with open(path_to_report_file, 'r') as report_file:
            soup = BeautifulSoup(report_file, 'lxml')
        table_body = soup.find('tbody')
        rows = table_body.find_all('tr')[4:]  # Start with data rows
        report = {}
        for index, row in enumerate(rows):
            report[index] = [cell.text.strip() for cell in row.find_all('td')]
        return report
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}


def get_report_date(mail_report: list, file_extension: str) -> str:
    if file_extension == '.html':
        report_date = mail_report[0][2]
    elif file_extension == '.xlsx':
        if mail_report[6][2] == "Профиль":
            report_date = mail_report[5][2]
        else:
            report_date = mail_report[6][2]
    else:
        raise ValueError(f"Unsupported file extension: {file_extension}")

    logger.info(report_date)
    return report_date


def main():
    path_to_report_file = select_file_via_gui()
    print(report_from_tass_mail(path_to_report_file)[0])


if __name__ == '__main__':
    print(report_from_tass_mail('../files_for_test/html_report.html'))
