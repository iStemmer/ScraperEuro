from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import csv

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

with open('all-dirk.csv') as file:
    content = file.readlines()
urls = content[1:]
i = 0
PRODUCT_COUNT_LIST = 10
rows = []
for url in urls:
    driver.get(url)
    attributes = []
    image_url = driver.find_element(By.CSS_SELECTOR, '.product-details__image img').get_attribute('src')
    attributes.append(driver.find_element(By.CSS_SELECTOR, '.product-details__info__title').text)
    attributes.append(driver.find_element(By.CSS_SELECTOR, '.product-details__info__subtitle').text)
    price = driver.find_element(By.CSS_SELECTOR, '.product-card__price__new').text
    attributes.append(price)
    #usual_price
    attributes.append(price)
    #discount
    attributes.append('null')
    #description
    attributes.append(driver.find_element(By.CSS_SELECTOR, '.product-details__extra__content').text)
    attributes.append(url)
    attributes.append(image_url)
    categories = driver.find_element(By.CLASS_NAME, 'bread-crumbs--list').text.splitlines()
    categories_text = []
    for category in categories:
        if category != 'f':
            categories_text.append(category)
    attributes.append("/".join(categories_text))
    attributes.append('Dirk')
    rows.append(attributes)
    i = i + 1
    if i == PRODUCT_COUNT_LIST:
        break

fieldnames = ['name', 'unit_info', 'price', 'usual_price', 'discount', 'description', 'url', 'image', 'categories',
              'store']

with open('prices-dirk.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(fieldnames)
    writer.writerows(rows)
