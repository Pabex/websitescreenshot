import io
import sys
import time
import imagehash
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
from urllib.parse import unquote


class Screenshot:
    def __init__(self, url, delay=2):
        self.url = url
        self.delay = delay
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--start-maximized")
        # https://stackoverflow.com/a/52340526/6696848
        options.add_argument("enable-automation")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-browser-side-navigation")
        options.add_argument("--disable-gpu")
        options.add_argument('--dns-prefetch-disable')  # https://sqa.stackexchange.com/a/17955
        self.driver = webdriver.Chrome('../chromedriver/chromedriver', options=options)
        self.driver.set_page_load_timeout(30)

        # Imagen en blanco
        white_image = Image.new("RGB", (100, 100), (255, 255, 255))
        self.hash_white_image = imagehash.average_hash(white_image)

    def save_image(self):
        self.driver.get(self.url)
        time.sleep(self.delay)
        self.driver.get_screenshot_as_file('screenshot_%s.png' % str(int(time.time())))
        self.driver.quit()
        return True

    def get_image(self):
        try:
            self.driver.get(self.url)
            time.sleep(self.delay)
            png = self.driver.get_screenshot_as_png()
            self.driver.quit()
            if self.__is_white_image(png):
                return False
            return png
        except Exception as e:
            print("Error en %s: " % self.url, str(e))
            self.driver.quit()
        return False

    def __is_white_image(self, bytes_image) -> bool:
        is_white = False
        with Image.open(io.BytesIO(bytes_image)) as image:
            hash_image = imagehash.average_hash(image)
            is_white = (self.hash_white_image - hash_image) == 0
        return is_white


if __name__ == '__main__':
    url = sys.argv[1]
    screenshot = Screenshot(url)
    screenshot.save_image()
