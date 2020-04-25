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
        self.driver = webdriver.Chrome('../chromedriver/chromedriver', options=options)

    def save_image(self):
        self.driver.get(self.url)
        time.sleep(self.delay)

        self.driver.get_screenshot_as_file('screenshot_%s.png' % str(int(time.time())))
        self.driver.quit()
        return True

    def get_image(self):
        self.driver.get(self.url)
        time.sleep(self.delay)
        png = self.driver.get_screenshot_as_png()
        return png


if __name__ == '__main__':
    url = sys.argv[1]
    screenshot = Screenshot(url)
    screenshot.save_image()
