import openpyxl


# create dict from xlsx file, index row number, value - list from columns date
def report_from_tass_xlsx_file(xlsx_file: str) -> dict:
    wb = openpyxl.load_workbook(xlsx_file)
    sheet = wb.active
    report = {}
    for number, value in enumerate(sheet.rows, start=1):
        report[number] = [cell.value if cell.value is not None else '' for cell in sheet[number]]
    return report


if __name__ == '__main__':
    print(report_from_tass_xlsx_file('../files_for_test/xlsx_report.xlsx'))
