import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
import time
driver_path = '/Users/msaad/Downloads/chromedriver'

options = Options()
options.add_argument('--headless')
options.add_argument("--window-size=1280,700")
options.add_argument('--ignore-certificate-errors')

driver = webdriver.Chrome(options= options, executable_path = driver_path)

driver.get('https://www.nofrills.ca/food/c/27985')
driver.implicitly_wait(40)
driver.find_element(By.XPATH, "//button[@class='modal-dialog__content__close']").click()

time.sleep(5)
cookies = WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='lds__privacy-policy__btnClose']")))
cookies.click()

count = 0
while count < 100 and driver.find_elements(By.XPATH, "//button[@class='primary-button primary-button--load-more-button']"):
    load_more = WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='primary-button primary-button--load-more-button']")))
    #driver.find_element(By.XPATH, "//button[@class='primary-button primary-button--load-more-button']").click()
    load_more.click()
    count += 1
    print(count)
    

foods = driver.find_elements(By.XPATH, "//span[@class='product-name__item product-name__item--name']")
prices = driver.find_elements(By.XPATH, "//span[@class='price__value selling-price-list__item__price selling-price-list__item__price--now-price__value']")
#print(len(foods), len(prices))
products_list = []

for i in range(len(foods)):
    products_list.append([foods[i].text, prices[i].text[1:]])

driver.quit()

nofrills_df = pd.DataFrame(products_list)
nofrills_df.columns = ['product', 'price']
nofrills_df = nofrills_df.reset_index(drop = True)
nofrills_df.to_csv('./nofrills_product_prices.csv', index = False)