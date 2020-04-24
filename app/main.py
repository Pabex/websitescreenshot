import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def download_image(url):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome('./chromedriver/chromedriver', options=options)

    driver.get(url)
    time.sleep(1)

    driver.get_screenshot_as_file('screenshot_%s.png' % str(int(time.time())))
    driver.quit()
    print("End..")


if __name__ == '__main__':
    url = sys.argv[1]
    download_image(url)