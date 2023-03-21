import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

driver_path = '/Users/msaad/Downloads/chromedriver'

options = Options()
options.add_argument('--headless')
options.add_argument("--window-size=1920,1200")
options.add_argument('--ignore-certificate-errors')

driver = webdriver.Chrome(options= options, executable_path = driver_path)
driver.get('https://www.metro.ca/en/online-grocery/search')

pages = driver.find_elements(By.CLASS_NAME, "ppn--short")[0].text
curPage, maxPage = int(pages.split('/')[0]), int(pages.split('/')[1])

products_list = []
while curPage < maxPage: #Getting everything will take a few minutes (LOTS OF PAGES)
    foods = driver.find_elements(By.CLASS_NAME, "head__title")
    prices = driver.find_elements(By.XPATH, "//div[@class = 'content__pricing']/div[@data-main-price]")
    for i in range(len(foods)):    # Since there is an equal amount of products and prices scraped
        products_list.append([foods[i].text, prices[i].get_attribute("data-main-price")])
    driver.find_elements(By.XPATH, "//a[@aria-label='Next']")[0].click
    curPage += 1
driver.quit()

metro_df = pd.DataFrame(products_list)
metro_df.columns = ['product', 'price']
metro_df = metro_df.reset_index(drop = True)
metro_df.to_csv('./metro_product_prices.csv', index = False)