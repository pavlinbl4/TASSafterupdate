import re
from bs4 import BeautifulSoup
from loguru import logger
from work_with_tass_sales_report.gui_select_file import select_file_via_gui


def report_from_tass_mail(path_to_report_file: str) -> dict:
    """Parse the sales report from an HTML file."""
    try:
        with open(path_to_report_file, 'r', encoding='utf-8') as report_file:
            soup = BeautifulSoup(report_file, 'lxml')

        table_body = soup.find('tbody')
        if not table_body:
            logger.error("No <tbody> found in the HTML report.")
            return {}

        rows = table_body.find_all('tr')
        if len(rows) <= 4:
            logger.warning("Insufficient rows in the table. Expected at least 5 rows.")
            return {}

        report = {}
        for index, row in enumerate(rows[4:]):  # Start with data rows
            cells = row.find_all('td')
            report[index] = [cell.text.strip() for cell in cells]
        return report
    except Exception as e:
        logger.error(f"An error occurred while parsing the report: {e}")
        return {}


def get_report_date(mail_report: dict, file_extension: str) -> str:
    """Extract the report date based on the file extension."""
    try:
        if file_extension == '.html':
            report_date = mail_report.get(0, [None])[2]
        elif file_extension == '.xlsx':
            row = mail_report.get(6, [None, None, None])
            if row[2] == "Профиль":
                report_date = mail_report.get(5, [None])[2]
            else:
                report_date = row[2]
        else:
            raise ValueError(f"Unsupported file extension: {file_extension}")

        if not report_date:
            raise ValueError("Report date not found.")

        logger.info(f"Extracted report date: {report_date}")
        return report_date.lower()
    except Exception as e:
        logger.error(f"Error in get_report_date: {e}")
        return ""


def get_year_from_report_date(report_date: str) -> str:
    """Extract the year from the report date."""
    match = re.search(r'\b\d{4}\b', report_date)
    if match:
        return match.group()
    logger.warning("No 4-digit year found in the report date.")
    return None


def main():
    try:
        path_to_report_file = select_file_via_gui()
        if not path_to_report_file:
            logger.warning("No file selected.")
            return

        report = report_from_tass_mail(path_to_report_file)
        if not report:
            logger.warning("No report data extracted.")
            return

        print(report.get(0, "No data in first row"))
    except Exception as e:
        logger.error(f"Error in main function: {e}")


if __name__ == '__main__':
    print(report_from_tass_mail('../files_for_test/html_report.html'))