import multiprocessing as mp
import os
import random
import sys
import time
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

PATH_DRIVER = './chromedriver-win64/chromedriver.exe'
URL = 'https://www.wildberries.ru/catalog/0/search.aspx?page=%d&sort=%s&search=%s'
PRODUCTS_PER_LOADED_PAGE = 100
PRODUCTS_PER_PAGE = 30


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


def get_info(valid_url: str) -> list:
    chrome_options = webdriver.ChromeOptions()
    user_agent = UserAgent().chrome
    chrome_options.add_argument(f'--user-agent={user_agent}')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--headless')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    service = Service(executable_path=resource_path(PATH_DRIVER))
    driver = webdriver.Chrome(options=chrome_options, service=service)
    driver.set_page_load_timeout(20)

    try:
        driver.get(url=valid_url)

        product_name = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'product-page__header')))
        button_id = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'productNmId')))
        id = button_id.get_attribute('textContent')
        rating = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'product-review__rating')))
        number_ratings = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'product-review__count-review')))
        old_price = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'price-block__old-price')))
        current_price = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'price-block__final-price')))

        res = [product_name.text, id, rating.text,
               number_ratings.text, old_price.text, current_price.text]
    except Exception as err:
        print(err)
        driver.quit()
        return [None, valid_url]
    
    driver.quit()
    return res


def get_valid_url(search_name: str, sort: str, page: int) -> str:
    search_name = search_name.replace(' ', '+')
    return URL % (page, sort, search_name)


def get_links(quantity: int, valid_url: str):
    chrome_options = webdriver.ChromeOptions()
    user_agent = UserAgent().chrome
    chrome_options.add_argument(f'--user-agent={user_agent}')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--headless')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    service = Service(executable_path=resource_path(PATH_DRIVER))
    driver = webdriver.Chrome(options=chrome_options, service=service)
    driver.set_page_load_timeout(20)

    try:
        driver.get(url=valid_url)
        time.sleep(3)

        time_ = 5
        if quantity > 30:
            height = driver.execute_script("return document.body.scrollHeight")
            if 30 < quantity <= 45:
                driver.execute_script(f"window.scrollTo(0, {height * 0.5});")  
                time.sleep(time_)
            elif 45 < quantity <= 60:
                driver.execute_script(f"window.scrollTo(0, {height * 0.5});")  
                time.sleep(time_)
                driver.execute_script(f"window.scrollTo(0, {height * 0.9});")  
                time.sleep(time_)
            elif 60 < quantity <= 75:
                driver.execute_script(f"window.scrollTo(0, {height * 0.5});") 
                time.sleep(time_)
                driver.execute_script(f"window.scrollTo(0, {height * 0.9});")  
                time.sleep(time_)
                driver.execute_script(f"window.scrollTo(0, {height * 1.3});")  
                time.sleep(time_)
            elif 75 < quantity <= 90:
                driver.execute_script(f"window.scrollTo(0, {height * 0.5});")  
                time.sleep(time_)
                driver.execute_script(f"window.scrollTo(0, {height * 0.9});")  
                time.sleep(time_)
                driver.execute_script(f"window.scrollTo(0, {height * 1.3});")  
                time.sleep(time_)
                driver.execute_script(f"window.scrollTo(0, {height * 1.7});")  
                time.sleep(time_)
            else:
                driver.execute_script(f"window.scrollTo(0, {height * 0.5});")  
                time.sleep(time_)
                driver.execute_script(f"window.scrollTo(0, {height * 0.9});")  
                time.sleep(time_)
                driver.execute_script(f"window.scrollTo(0, {height * 1.3});")  
                time.sleep(time_)
                driver.execute_script(f"window.scrollTo(0, {height * 1.7});")  
                time.sleep(time_)
                driver.execute_script(f"window.scrollTo(0, {height * 2.1});")  
                time.sleep(time_)

        goods = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'product-card__link')))
        links = [good.get_attribute('href') for index, good in enumerate(goods, start=1) if index <= quantity]
    except Exception as err:
        print(err)
        driver.quit()
        return [None]
    
    time.sleep(random.randrange(1, 15))
    driver.quit()
    return links


def extract_data(search_name: str, sort: str, quantity: int) -> list:
    # mp.freeze_support()
    args = [(PRODUCTS_PER_LOADED_PAGE, get_valid_url(search_name, sort, i+1)) for i in range(quantity // PRODUCTS_PER_LOADED_PAGE)]
    if quantity % PRODUCTS_PER_LOADED_PAGE != 0:
        args.append((quantity % PRODUCTS_PER_LOADED_PAGE, get_valid_url(search_name, sort, len(args)+1)))

    try:
        with mp.Pool(processes=mp.cpu_count()) as p:
            result = p.starmap(get_links, args)
    except Exception as err:
        print(err)        
        
    new_args = [i for sublist in result for i in sublist]
    try:
        with mp.Pool(processes=mp.cpu_count()) as p:
            new_result = p.map(get_info, new_args)
    except Exception as err:
        print(err)
        
    return new_result


if __name__ == "__main__":
    data = extract_data('Iphone 12', 'popular', 134)