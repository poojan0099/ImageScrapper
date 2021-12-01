import io
import time
from selenium.webdriver.common.by import By
from selenium import webdriver
import requests
import os
from PIL import Image

rootPath = os.path.abspath(os.path.dirname(__file__))
driverPath = os.path.join(rootPath, 'chromedriver.exe')
driver = webdriver.Chrome(driverPath)


def get_images_google(driver, delay, max_images):
    def scroll_down(driver):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

    url = "https://www.google.com/search?q=dragon+ball&rlz=1C1CHBD_enIN840IN840&hl=en&sxsrf=AOaemvLuEeMADrjQVRrwYU0rZKCPQiYzNg:1637150269929&source=lnms&tbm=isch&sa=X&ved=2ahUKEwi-raGCrJ_0AhU273MBHWDDAn8Q_AUoAnoECAEQBA&biw=1366&bih=635&dpr=1"
    driver.get(url)

    image_url = set()

    while len(image_url) < max_images:
        scroll_down(driver)

        thumbnails = driver.find_elements(By.CLASS_NAME, "Q4LuWd")

        for img in thumbnails[len(image_url): max_images]:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue

            images = driver.find_elements(By.CLASS_NAME, "n3VNCb")
            for image in images:
                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_url.add(image.get_attribute('src'))
                    print(f"Found {len(image_url)}")

    return image_url


def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")

        print("Success")
    except Exception as e:
        print('FAILED -', e)


urls = get_images_google(driver, 1, 10)

for i, url in enumerate(urls):
    download_image("images/", url, str(i) + ".jpg")

driver.quit()
