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


def download_photo_preview_by_id(photo_id, path_to_download='test_downloads'):
    driver.get(f'https://www.tassphoto.com/ru/asset/fullTextSearch/search/{photo_id}/page/1')
    WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.ID, "userrequest"))
    )
    picture = driver.find_element(By.CSS_SELECTOR, f"img.thumb{photo_id}").get_attribute("src")
    print(picture)
    get_image = requests.get(picture)
    os.makedirs(path_to_download,
                exist_ok=True)
    with open(
            f"{path_to_download}/{photo_id}.jpg",
            'wb') as img_file:
        img_file.write(get_image.content)


if __name__ == '__main__':
    download_photo_preview_by_id(photo_id='75520997')