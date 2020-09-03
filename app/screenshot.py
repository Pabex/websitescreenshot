import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


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
        self.driver = webdriver.Chrome('../chromedriver/chromedriver', options=options)
        self.driver.set_page_load_timeout(20)

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
            return png
        except Exception as e:
            print("Error en %s: " % self.url, str(e))
            self.driver.quit()
        return False


if __name__ == '__main__':
    url = sys.argv[1]
    screenshot = Screenshot(url)
    screenshot.save_image()
