import multiprocessing as mp
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

URL = 'https://www.wildberries.ru/catalog/0/search.aspx?page=1&sort=%s&search=%s'


def extract_data(search_name: str, quantity: int, sort: str) -> list:
    url = URL % (sort, search_name)
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
    try:
        driver.get(url=url)

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
    finally:
        driver.quit()
    return res


if __name__ == "__main__":
    data = extract_data('samsung', 15, 'popular')
    print(data)
    print(len(data))