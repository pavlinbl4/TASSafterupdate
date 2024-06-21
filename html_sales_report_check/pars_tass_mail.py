from bs4 import BeautifulSoup

from gui_select_file import select_file_via_gui


# from html report file extract dict with information about sales
def report_from_tass_mail(mail_as_html: str) -> dict:
    with open(mail_as_html, 'r') as report_file:
        table = BeautifulSoup(report_file, 'lxml')
    table = table.find('tbody')
    table = table.find_all('tr')[4:]  # start with data row in table
    row_in_table = [x for x in table]
    report = {}
    for i in range(len(table)):
        report[i] = [x.text.strip() for x in row_in_table[i].find_all('td')]
    return report


def get_report_date(mail_report):
    return mail_report[0][2]


def main():
    path_to_report_file = select_file_via_gui()
    print(report_from_tass_mail(path_to_report_file)[0])
