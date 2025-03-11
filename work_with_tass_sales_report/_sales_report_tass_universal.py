"""
Главный модуль программы для обработки отчета от ТАСС.
Вносит данные о продаже в единый файл и скачивает превью купленных снимков
"""

from pathlib import Path
from tkinter import filedialog
from typing import Optional, Dict

from loguru import logger

from work_with_tass_sales_report.pars_tass_mail import report_from_tass_mail, get_report_date
from work_with_tass_sales_report.prevue_downloader import get_preview_mail_report
from work_with_tass_sales_report.write_to_xlsx import write_to_main_file
from work_with_tass_sales_report.data_from_report import get_info_from_report
from work_with_tass_sales_report.extract_dict_from_xlsx_report import report_from_tass_xlsx_file

# Константы
ICLOUD_FOLDER = Path.home() / 'Library/Mobile Documents/com~apple~CloudDocs/Documents'
MAIN_REPORT = ICLOUD_FOLDER / 'TASS/all_years_report.xlsx'
"""/Users/evgeniy/Library/Mobile Documents/com~apple~CloudDocs/Documents"""

def tass_sales():
    """Главная функция обработки отчета ТАСС."""
    try:
        file_dialog = filedialog.askopenfile()
        if not file_dialog:
            logger.error("Файл не выбран.")
            return

        path_to_report_file = file_dialog.name

        # Проверяем расширение файла
        file_extension = Path(path_to_report_file).suffix.lower()
        logger.info(f"Выбран файл: {path_to_report_file}, расширение: {file_extension}")

        mail_report = extract_mail_report(file_extension, path_to_report_file)
        if not mail_report:
            logger.error("Не удалось обработать файл отчета. Проверьте формат.")
            return

        # Получаем дату из отчета
        report_date = get_report_date(mail_report, file_extension)
        logger.info(f"Дата отчета: {report_date}")

        # Формируем словарь с данными о продажах
        photos_report = get_info_from_report(mail_report, file_extension)
        logger.debug(f"Сформирован отчет о продажах: {photos_report}")

        # Записываем в основной файл
        write_to_main_file(photos_report, MAIN_REPORT, report_date)

        # Скачиваем превью
        get_preview_mail_report(photos_report, report_date)

        logger.info("Обработка отчета завершена успешно.")

    except Exception as e:
        logger.exception(f"Ошибка при обработке отчета: {e}")


def extract_mail_report(file_extension: str, path_to_report_file: str) -> Optional[Dict]:
    """Извлечение данных из файла отчета в зависимости от расширения."""
    try:
        if file_extension == '.html':
            return report_from_tass_mail(path_to_report_file)
        elif file_extension == '.xlsx':
            return report_from_tass_xlsx_file(path_to_report_file)
        else:
            logger.error(f"Неподдерживаемый тип файла: {file_extension}")
            return None
    except Exception as e:
        logger.exception(f"Ошибка при извлечении данных из файла {path_to_report_file}: {e}")
        return None


if __name__ == '__main__':
    tass_sales()