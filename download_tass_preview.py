"""
Функция принимает photo_id и путь к сохраняемому файлу (так как файл может сохраняться
под другим именем
"""

import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from must_have.crome_options import setting_chrome_options
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


def download_photo_preview_by_id(photo_id: str, picture_folder_downloads: str, image_file_name=None):
    # Установка имени файла по умолчанию
    image_file_name = image_file_name if image_file_name else f"{photo_id}.jpg"
    image_path = os.path.join(picture_folder_downloads, image_file_name)

    # Создание папки для загрузок (если её нет)
    os.makedirs(picture_folder_downloads, exist_ok=True)

    # Настройка драйвера
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=setting_chrome_options())

    try:
        # Открытие страницы с фотографией
        driver.get(f'https://www.tassphoto.com/ru/asset/fullTextSearch/search/{photo_id}/page/1')
        WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.ID, "userrequest"))
        )

        # Поиск элемента изображения по селектору
        picture_element = driver.find_element(By.CSS_SELECTOR, f"img.thumb-{photo_id}")
        picture_url = picture_element.get_attribute("src")

        # Загрузка изображения через requests
        image_response = requests.get(picture_url)
        if image_response.status_code != 200:
            raise Exception(f"Failed to download image. Status code: {image_response.status_code}")

        # Сохранение изображения на диск
        with open(image_path, 'wb') as img_file:
            img_file.write(image_response.content)

        print(f"Image successfully saved to {image_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Закрытие драйвера
        driver.quit()


if __name__ == '__main__':

    download_photo_preview_by_id('73669467', 'test_downloads', 'October_best_picture.jpg')
