from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import csv

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

with open('all-ah.csv') as file:
    content = file.readlines()
urls = content[1:]
i = 0
PRODUCT_COUNT_LIST = 10
rows = []
for url in urls:
    driver.get(url)
    attributes = []
    my_attributes = driver.find_element(By.CSS_SELECTOR, '[data-testhook="product-card"]').text.splitlines()
    image_url = driver.find_element(By.CSS_SELECTOR, 'img[data-testhook="product-image"]').get_attribute('src')
    categories = driver \
        .find_element(By.CSS_SELECTOR, '[data-testhook="breadcrumb-nav"]') \
        .find_elements(By.CSS_SELECTOR, '[data-testhook="breadcrumb-item"]')
    if my_attributes[1] != 'korting':
        # name
        attributes.append(my_attributes[0])
        # unit_info
        attributes.append(my_attributes[1])
        # price
        attributes.append(my_attributes[2])
        # usual_price
        attributes.append(my_attributes[2])
        # discount
        attributes.append('null')
        # description
        # skip button Voeg toe
        attributes.append(" ".join(my_attributes[5:]))
    else:
        # name
        attributes.append(my_attributes[2])
        # unit_info
        attributes.append(my_attributes[3])
        # price
        attributes.append(my_attributes[my_attributes.index('Voeg toe') - 1])
        # usual_price
        attributes.append(my_attributes[my_attributes.index('Voeg toe') - 2])
        # discount
        attributes.append(my_attributes[0])
        # description
        # skip button Voeg toe
        attributes.append(" ".join(my_attributes[my_attributes.index('Voeg toe') + 1:]))
    attributes.append(url)
    attributes.append(image_url)
    categories_text = []
    for category in categories:
        categories_text.append(category.text)

    attributes.append("/".join(categories_text))
    attributes.append('Albert Heijn')
    rows.append(attributes)
    i = i + 1
    if i == PRODUCT_COUNT_LIST:
        break

fieldnames = ['name', 'unit_info', 'price', 'usual_price', 'discount', 'description', 'url', 'image', 'categories',
              'store']

with open('prices.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(fieldnames)
    writer.writerows(rows)
