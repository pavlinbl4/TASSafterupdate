from bs4 import BeautifulSoup


def report_from_tass_mail(mail_as_html):
    with open(mail_as_html, 'r') as report_file:
        table = BeautifulSoup(report_file, 'lxml')
    table = table.find('tbody')
    table = table.find_all('tr')[4:]  # start with data row in table
    row_in_table = [x for x in table]
    report = {}
    for i in range(len(table)):
        report[i] = [x.text.strip() for x in row_in_table[i].find_all('td')]
    return report


if __name__ == '__main__':
    print(report_from_tass_mail("/Users/evgeniy/Downloads/Gmail - Отчет по продажам июнь_ТАСС.html")[2])
