"""
Главный модуль программы для обработки отчета от ТАСС.
Вносит данные о продаже в единый файл и скачивает превью купленных снимков
"""

from pathlib import Path
from tkinter import filedialog
from typing import Optional, Dict

from loguru import logger

from core.config_loader import ConfigLoader
from work_with_tass_sales_report.data_from_report import get_info_from_report
from work_with_tass_sales_report.extract_dict_from_xlsx_report import report_from_tass_xlsx_file
from work_with_tass_sales_report.prevue_downloader import get_preview_mail_report
from work_with_tass_sales_report.write_to_xlsx import write_to_main_file

# Константы
config = ConfigLoader.load("TASS")
ICLOUD_FOLDER = Path.home() / config['ICLOUD_FOLDER']
MAIN_REPORT = ICLOUD_FOLDER / 'TASS/all_years_report.xlsx'


def tass_sales():
    """Главная функция обработки отчета ТАСС."""
    try:
        file_dialog = filedialog.askopenfile()
        if not file_dialog:
            logger.error("Файл не выбран.")
            return

        path_to_report_file = file_dialog.name

        dict_report_from_xlsx = extract_xlsx_report(path_to_report_file)
        if not dict_report_from_xlsx:
            logger.error("Не удалось обработать файл отчета. Проверьте формат.")
            return

        # Получаем дату из отчета
        report_date = dict_report_from_xlsx[6][2]
        logger.info(f"Дата отчета: {report_date}")

        # Формируем словарь с данными о продажах
        photos_report = get_info_from_report(dict_report_from_xlsx)
        logger.debug(f"Сформирован отчет о продажах: {photos_report}")

        # Записываем в основной файл
        write_to_main_file(photos_report, MAIN_REPORT, report_date)
        logger.info("Report added to main file")

        # Скачиваем превью
        logger.info("Start to download preview")
        get_preview_mail_report(photos_report, report_date)

        logger.info("Обработка отчета завершена успешно.")

    except Exception as e:
        logger.exception(f"Ошибка при обработке отчета: {e}")


def extract_xlsx_report(path_to_report_file: str) -> Optional[Dict]:
    file_extension = Path(path_to_report_file).suffix.lower()

    if file_extension == '.xlsx':
        return report_from_tass_xlsx_file(path_to_report_file)
    else:
        logger.error(f"Неподдерживаемый тип файла: {file_extension}")
        return None


if __name__ == '__main__':
    tass_sales()
