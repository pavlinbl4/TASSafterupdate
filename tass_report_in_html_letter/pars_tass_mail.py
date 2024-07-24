from bs4 import BeautifulSoup
from work_with_tass_sales_report.gui_select_file import select_file_via_gui
from loguru import logger


# from html report file extract dict with information about sales,
# index row number, value - list from columns date
def report_from_tass_mail(path_to_report_file: str) -> dict:
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


def main():
    path_to_report_file = select_file_via_gui()
    print(report_from_tass_mail(path_to_report_file)[0])


if __name__ == '__main__':
    print(report_from_tass_mail('../files_for_test/html_report.html'))
