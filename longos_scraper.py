import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
driver_path = '/Users/msaad/Downloads/chromedriver'

options = Options()
#options.add_argument('--headless')
#options.add_argument("--window-size=1280,700")
options.add_argument('--ignore-certificate-errors')

driver = webdriver.Chrome(options= options, executable_path = driver_path)
driver.maximize_window()
actions = ActionChains(driver)

driver.get('https://www.longos.com/Fresh-Fruits-and-Vegetables/c/701')
driver.implicitly_wait(20)


#print(results_shown.split(" "))

products = []

#print(currentlyShown, maxShown)
categories = driver.find_elements(By.XPATH, "//div[@class = 'navbar d-flex']/gg-menu-dropdown")

#next_cat = button.find_element(By.XPATH, "./../div/ul/li/a[@innerText = ' SEE ALL ']")
#print(next_cat)

#print(next_button)
#next_button.click()
#print(len(categories))



for i in range(len(categories) - 1):
    time.sleep(2)
    if not i == 0:
        button = categories[i].find_element(By.XPATH, "./div/button")
        button.click()
        next_button = categories[i].find_element(By.XPATH, "./div/div/ul/li[1]/a")
        next_button.click()

    time.sleep(3)
    results_shown = driver.find_element(By.XPATH, "//gg-product-filters/div/div[@class='d-none d-xl-flex filters-items-counter']").get_attribute("textContent")
    currentlyShown = int(results_shown.split(" ")[2])
    maxShown = int(results_shown.split(" ")[4])
    actions.send_keys(Keys.TAB).perform() # For some reason it won't perform the ctrl+end the first time unless I do this?
    while currentlyShown < maxShown:
        actions.key_down(Keys.CONTROL).send_keys(Keys.END).perform()
        #driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(2)
        load_more = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div/button[@class='btn-black']")))
        load_more.click()
        time.sleep(1)
        currentlyShown = int(driver.find_element(By.XPATH, "//gg-product-filters/div/div[@class='d-none d-xl-flex filters-items-counter']").get_attribute("textContent").split(" ")[2])
        #print(currentlyShown)

    # TODO NEXT: Get food and prices, then look into switching categories
    #foods = driver.find_elements(By.XPATH, "//h5[@class ='card-title mb-0']")
    #prices_no_sale = driver.find_elements(By.XPATH, "//strong[@class = 'price']")

    prices_no_sale = driver.find_elements(By.XPATH, "//strong[@class = 'price']")
    prices_sale = driver.find_elements(By.XPATH, "//strong[@class = 'price text-primary']")

    for price in prices_no_sale:
        cost = price.get_attribute('textContent')
        cost = cost[2:]
        cost = cost[:-3] + '.' + cost[-3:-1]
        food = price.find_element(By.XPATH, "./../../../../div[@class = 'card-body flex-grow-1']/a/h5").get_attribute('textContent')
        products.append([food, cost])
    for price in prices_sale:
        cost = price.get_attribute('textContent')
        cost = cost[2:]
        cost = cost[:-3] + '.' + cost[-3:-1]
        food = price.find_element(By.XPATH, "./../../../../div[@class = 'card-body flex-grow-1']/a/h5").get_attribute('textContent')
        products.append([food, cost])


print(len(products))

driver.quit()

longos_df = pd.DataFrame(products)
longos_df.columns = ['product', 'price']
longos_df = longos_df.reset_index(drop = True)
longos_df.to_csv('./longos_product_prices.csv', index = False)