import multiprocessing as mp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

URL = 'https://www.wildberries.ru/'


def extract_data(search_name: str, index: int, lock=mp.Lock()):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--remote-debugging-port=0')
    service = webdriver.ChromeService(port=0)
    driver = webdriver.Chrome(options=chrome_options, service=service)
    try:
        driver.get(url=URL)
        time.sleep(5)

        # search = WebDriverWait(driver, 20).until(
        #     EC.element_to_be_clickable((By.ID, 'searchInput')))

        search = driver.find_element(By.ID, 'searchInput')
        search.send_keys(search_name)
        search.send_keys(Keys.ENTER)
        time.sleep(5)

        if index > 29:
            driver.execute_script(
                "window.scrollBy(0,document.body.scrollHeight)")

        goods = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'product-card')))
        goods[index].click()

        # driver.save_screenshot(f'{index}_1_screen.png')
        product_name = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'product-page__header')))

        # button_id = WebDriverWait(driver, 20).until(
        #     EC.presence_of_element_located((By.ID, 'productNmId')))
        # id = button_id.get_attribute('textContent')
        # popup = WebDriverWait(driver, 20).until(
        #     EC.presence_of_element_located((By.CLASS_NAME, 'popup__content')))
        # if popup.is_displayed():
        #     webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()


        rating = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'product-review__rating')))


        number_ratings = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'product-review__count-review')))


        old_price = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'price-block__old-price')))


        current_price = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'price-block__final-price')))
        
        # driver.save_screenshot(f'{index}_0_screen.png')
            
        # product_name = driver.find_element(
        #     By.CLASS_NAME, 'product-page__header')
        # button_id = driver.find_element(By.ID, 'productNmId')
        # id = button_id.get_attribute('textContent')
        # rating = driver.find_element(
        #     By.CLASS_NAME, 'product-review__rating')
        # number_ratings = driver.find_element(
        #     By.CLASS_NAME, 'product-review__count-review')
        # old_price = driver.find_element(
        #     By.CLASS_NAME, 'price-block__old-price')
        # current_price = driver.find_element(
        #     By.CLASS_NAME, 'price-block__final-price')
            

        with lock:
            print(f'INDEX {index}\nНазвание: {product_name.text}\nАртикул: {id}\nРейтинг: {rating.text} \
                    \nКоличество отзывов: {number_ratings.text}\nСтарая цена: {old_price.text} \
                    \nТекущая цена: {current_price.text}')
            print()

    except Exception as err:
        print(err)
    finally:
        # driver.close()
        driver.quit()


if __name__ == "__main__":
    # extract_data('iphone', 0)
    # extract_data('iphone', 1)
    # extract_data('iphone', 2)
    # extract_data('iphone', 3)
    # extract_data('iphone', 4)
    # extract_data('iphone', 5)
    # extract_data('iphone', 6)
    # extract_data('iphone', 7)
    # extract_data('iphone', 8)
    # extract_data('iphone', 9)   
    # extract_data('iphone', 10)
    # extract_data('iphone', 11)
    # extract_data('iphone', 12)
    # extract_data('iphone', 13)
    # extract_data('iphone', 14)
    # extract_data('iphone', 15)
    # extract_data('iphone', 16) 
    # extract_data('iphone', 17)
    # extract_data('iphone', 18)
    # extract_data('iphone', 19)   

    # extract_data('iphone', 0)
    # extract_data('iphone', 1)
    # extract_data('iphone', 2)
    # extract_data('iphone', 3)
    # extract_data('iphone', 4)
    # extract_data('iphone', 5)
    # extract_data('iphone', 6)
    # extract_data('iphone', 7)
    # extract_data('iphone', 8)
    # extract_data('iphone', 9)   
    # extract_data('iphone', 10)
    # extract_data('iphone', 11)
    # extract_data('iphone', 12)
    # extract_data('iphone', 13)
    # extract_data('iphone', 14)
    # extract_data('iphone', 15)
    # extract_data('iphone', 16) 
    # extract_data('iphone', 17)
    # extract_data('iphone', 18)
    # extract_data('iphone', 19)         
    numbers = [('iphone', i) for i in range(10)]
    with mp.Pool(processes=mp.cpu_count()) as p:
        p.starmap(extract_data, numbers)
