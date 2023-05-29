from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time


def setting_chrome_options():
    chrome_options = Options()
    chrome_options.add_experimental_option('detach', True)  # if browser close
    chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument("--headless")  # фоновый режим
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # невидимость автоматизации
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
    return chrome_options


if __name__ == '__main__':
    try:
        browser = webdriver.Chrome(options=setting_chrome_options())
        browser.get('https://chromedriver.chromium.org/')
        time.sleep(5)
        browser.close()
        browser.quit()
    except Exception as e:
        print(e)
