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

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=setting_chrome_options())


def download_photo_preview_by_id(photo_id: str, image_path: str):
    driver.get(f'https://www.tassphoto.com/ru/asset/fullTextSearch/search/{photo_id}/page/1')
    WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.ID, "userrequest"))
    )

    picture_element = driver.find_element(By.CSS_SELECTOR, f"img.thumb{photo_id}")
    picture_url = picture_element.get_attribute("src")

    image_response = requests.get(picture_url)

    with open(image_path, 'wb') as img_file:
        img_file.write(image_response.content)


if __name__ == '__main__':
    picture_folder = 'test_downloads'
    image_file_name = 'renamed_jpeg_image.jpg'
    _image_path = os.path.join(picture_folder, image_file_name)
    os.makedirs(picture_folder,
                exist_ok=True)
    download_photo_preview_by_id('75520997', _image_path)
