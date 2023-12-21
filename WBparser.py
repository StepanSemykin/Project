import multiprocessing as mp
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

URL = 'https://www.wildberries.ru/catalog/0/search.aspx?page=1&sort=%s&search=%s'
PRODUCTS_PER_PAGE = 99
GOODS_PER_PAGE = 29


def get_valid_url(search_name: str, sort: str) -> str:
    search_name = search_name.replace(' ', '+')
    return URL % (sort, search_name)


def get_valid_index(index: int) -> int:
    return int(str(index)[-2:])


def extract_data(search_name: str, quantity: int, sort: str) -> list:
    url = get_valid_url(search_name, sort)
    args = [(url, i) for i in range(quantity)]
    results_list = []
    with mp.Pool(processes=mp.cpu_count()) as p:
        result = p.starmap(get_info, args)
        results_list.append(result)
    return results_list[0]


def get_info(url: str, index: int) -> list:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--remote-debugging-port=0')
    service = webdriver.ChromeService(port=0)
    driver = webdriver.Chrome(options=chrome_options, service=service)
    driver.set_page_load_timeout(20)

    page = str((index // PRODUCTS_PER_PAGE) + 1)
    valid_url = url.replace('1', page)
    try:
        driver.get(url=valid_url)

        if index > GOODS_PER_PAGE:
            index = get_valid_index(index)
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight") 
            driver.execute_script(f"window.scrollTo(0, {new_height * 0.5});")
            time.sleep(3)
            driver.execute_script(f"window.scrollTo({new_height * 0.5}, {new_height * 0.9});")
            time.sleep(3)
            driver.execute_script(f"window.scrollTo({new_height * 0.9}, {new_height * 1.2});")
            time.sleep(3)
            driver.execute_script(f"window.scrollTo({new_height * 1.2}, {new_height * 1.4});")
            time.sleep(3)
            driver.execute_script(f"window.scrollTo({new_height * 1.4}, {new_height * 1.8});")
            time.sleep(3)   

        goods = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'product-card')))
        goods[index].click()

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
        return [None, index]  
    driver.quit()
    return res


if __name__ == "__main__":
    data = extract_data('Iphone 12', 25, 'popular')
    print(data)
