from selenium import webdriver
import time

#specify where your chrome driver present in your pc
PATH=r"C:\Users\educative\Documents\chromedriver\chromedriver.exe"

#get instance of web driver
driver = webdriver.Chrome(PATH)

#provide website url here
driver.get("https://omayo.blogspot.com/")

#sleep for 2 seconds
time.sleep(2)

#click on the link to get popup
popup_link = driver.find_element("xpath", '//*[@id="HTML37"]/div[1]/p/a').click()

#get instance of first pop up  window
whandle = driver.window_handles[1]

#switch to pop up window
driver.switch_to.window(whandle)

#get text of a element in pop window
print(driver.find_element("id","para1").text)

#sleep for 1 second
time.sleep(1)

#closes current window
driver.close()