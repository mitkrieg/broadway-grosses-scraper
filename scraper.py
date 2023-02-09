from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import codecs
import re
from webdriver_manager.chrome import ChromeDriverManager

driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))

url = 'https://www.broadwayleague.com/research/grosses-broadway-nyc/'
wait = WebDriverWait(driver,10)
driver.get(url)
get_url = driver.current_url
wait.until(EC.url_to_be(url))

if get_url == url:
    page = driver.page_source
    
search = driver.find_element(by=By.XPATH, value="//div[@class='search-box']")
search.click()

week_of_start = driver.find_element(by=By.ID, value='id_start_week_date')
week_of_start.send_keys("02/14/2016")

week_of_end = driver.find_element(by=By.ID, value='id_end_week_date')
week_of_end.send_keys("02/14/2016")
week_of_end.send_keys(Keys.RETURN)

results = driver.find_elements(by=By.CLASS_NAME, value="search-info")
raw_data = [r.get_attribute('innerHTML') for r in results]