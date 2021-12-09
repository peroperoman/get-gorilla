import os
import urllib.request
from selenium import webdriver
from time import sleep

save_dir = 'gorilla_images'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

url = 'https://search.yahoo.co.jp/image/search?ei=UTF-8&fr=mcafeess1&p=%E3%82%B4%E3%83%AA%E3%83%A9'
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(
    executable_path='/Users/katsuo-pc/webdriver/chromedriver',
    options=options)

driver.get(url)
driver.implicitly_wait(2)

while True:
    height = driver.execute_script('return document.body.scrollHeight')
    driver.execute_script(f'window.scrollTo(0, {height})')
    sleep(2)

    try:
        more_button = driver.find_element_by_css_selector('div.sw-MoreButton > div > button')
        more_button.click()
    except:
        new_height = driver.execute_script('return document.body.scrollHeight')
        if height == new_height:
            break

img_tags = driver.find_elements_by_css_selector('div.sw-Thumbnail.sw-Thumbnail--tile > figure > a > img')
for idx, img_tag in enumerate(img_tags):
    img_url = img_tag.get_attribute('src')
    img_name = os.path.basename(img_url)
    img_data = urllib.request.urlopen(img_url).read()
    try:
        with open(f'{save_dir}/{idx}_{img_name}', mode="wb") as f:
            f.write(img_data)
    except OSError as e:
        if e.errno == 63:
            _, img_ex = os.path.splitext(img_name)
            with open(f'{save_dir}/{idx}{img_ex}', mode="wb") as f:
                f.write(img_data)
        else:
            pass

driver.quit()
