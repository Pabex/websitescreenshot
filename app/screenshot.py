import io
import os
import sys
import time
import imagehash
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image


class Screenshot:
    def __init__(self, url, delay=2, headless=True):
        self.url = url
        self.delay = delay
        options = Options()
        if headless:
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
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36")
        prefs = {"profile.default_content_setting_values.notifications": 2}
        options.add_experimental_option("prefs", prefs)
        options.add_argument("user-data-dir=data_chrome")
        self.driver = webdriver.Chrome('../chromedriver/chromedriver', options=options)
        self.driver.set_window_size(1280, 720)
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
        png = None
        try:
            if "facebook.com" in self.url:
                png = self.facebook()
            elif "instagram.com" in self.url:
                png = self.instagram()
            else:
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
        return png

    def facebook(self):
        self.driver.set_page_load_timeout(60)
        self.driver.get(self.url)
        time.sleep(6)

        def login_facebook():
            txt_email = self.driver.find_element(By.ID, "email")
            txt_password = self.driver.find_element(By.ID, "pass")
            email = os.environ.get("EMAIL_FACEBOOK")
            password = os.environ.get("PASSWORD_FACEBOOK")
            time.sleep(4)
            txt_email.clear()
            txt_email.send_keys(email)

            txt_password.send_keys(password)
            txt_password.send_keys(Keys.ENTER)
            time.sleep(2)
            try:
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/']")))
            except:
                pass

        if len(self.driver.find_elements(By.ID, "email")) > 0 and len(self.driver.find_elements(By.ID, "pass")) > 0:
            # Esta en el login, tenemos que iniciar sesion.
            login_facebook()
        elif len(self.driver.find_elements(By.CSS_SELECTOR, "div[aria-label='No iniciaste sesión'")) > 0:
            self.driver.get("https://www.facebook.com")
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "email")))
            login_facebook()
            self.driver.get(self.url)
        elif "Escribe tu contraseña" in self.driver.page_source:
            time.sleep(3)
            txt_password = self.driver.find_element(By.ID, "pass")
            password = os.environ.get("PASSWORD_FACEBOOK")
            txt_password.send_keys(password)
            txt_password.send_keys(Keys.ENTER)
            time.sleep(3)

        png = self.driver.get_screenshot_as_png()
        return png

    def instagram(self):
        self.driver.set_page_load_timeout(60)
        self.driver.get(self.url)
        time.sleep(6)

        email_instagram = os.environ.get("EMAIL_INSTAGRAM")
        password_instagram = os.environ.get("PASSWORD_INSTAGRAM")

        if len(self.driver.find_elements(By.CSS_SELECTOR, "input[name='username']")) > 0 and len(self.driver.find_elements(By.CSS_SELECTOR, "input[name='password']")):
            # Esta en el login, tenemos que iniciar sesion.
            txt_username = self.driver.find_element(By.CSS_SELECTOR, "input[name='username']")
            txt_password = self.driver.find_element(By.CSS_SELECTOR, "input[name='password']")
            time.sleep(4)
            txt_username.send_keys(email_instagram)
            txt_password.send_keys(password_instagram)
            txt_password.send_keys(Keys.ENTER)
            time.sleep(4)

        WebDriverWait(self.driver, 20, ignored_exceptions=True).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "img[data-testid='user-avatar']")))

        png = self.driver.get_screenshot_as_png()

        return png

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
