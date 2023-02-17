from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import date, timedelta
import re
import time
import pandas as pd
import random
from webdriver_manager.chrome import ChromeDriverManager

timer = time.time()

options = Options()
options.add_argument('--headless')

driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
url = 'https://www.broadwayleague.com/research/grosses-broadway-nyc/'
wait = WebDriverWait(driver,10)
driver.get(url)

start_date = date(1980,6,8)
end_date = date.today()
all_dates = [start_date + timedelta(days=7*(x+1)) for x in range((end_date - start_date).days // 7)]
dates = [d.strftime('%m/%d/%Y') for d in all_dates if d <= date(2020,3,8) or d >= date(2021,8,8)]

all_cols = ['week_of','show_name','show_type','theatre','num_previews','num_performances',
               'grosses','grosses_prev','attendance','attend_prev','pct_capacity'
           ]

cols = [col for col in all_cols if col.endswith('_prev') == False]
                 

shows = pd.DataFrame(columns=cols)
weekly = []

for week in dates:
    print(f'getting {week}')
    get_url = driver.current_url
    # wait.until(EC.url_to_be(url))

    if get_url == url:
        page = driver.page_source

    search = driver.find_element(by=By.XPATH, value="//div[@class='search-box']")
    search.click()

    week_of_start = driver.find_element(by=By.ID, value='id_start_week_date')
    week_of_start.clear()

    week_of_start.send_keys(week)

    week_of_end = driver.find_element(by=By.ID, value='id_end_week_date')
    week_of_end.clear()
    week_of_end.send_keys(week)
    week_of_end.send_keys(Keys.RETURN)

    results = driver.find_elements(by=By.CLASS_NAME, value="search-info")
    raw_data = [r.get_attribute('innerHTML') for r in results]
    week_of = [i.strip() for i in raw_data[0].split('thru')][0]
    del raw_data[0]
    parse = [re.sub('[ $,]','',i).lower().split(':') for i in raw_data]
    data = {parsed[0]:parsed[1] for parsed in parse}
    data['week_of'] = week_of
    weekly.append(data)
    
    table_element = driver.find_elements(by=By.XPATH,value="//tr[@class='odd' or @class='even']") 
    table = pd.DataFrame([BeautifulSoup(t.get_attribute('innerHTML').strip(),'html.parser').find_all('td') for t in table_element],columns=all_cols)
    shows = pd.concat([shows,table[cols]])
    time.sleep(random.randint(0, 3))

shows = shows.applymap(lambda x:x.getText())
shows.week_of = pd.to_datetime(shows.week_of)
shows.grosses = shows.grosses.str.replace('[ $,]','',regex=True).astype(float)
shows.attendance = shows.attendance.str.replace('[ $,]','',regex=True).astype(int)
shows.num_performances = shows.num_performances.astype(int)
shows.num_previews = shows.num_previews.astype(int)
shows.pct_capacity = shows.pct_capacity.str.replace('[ %]','',regex=True).astype(float) / 100
shows.to_csv('./data/shows.csv',header=True, index=False)

weeks = pd.DataFrame(weekly)
weeks.totalentries = weeks.totalentries.astype(int)
weeks.totalgross = weeks.totalgross.astype(float)
weeks.totalattendance = weeks.totalattendance.astype(int)
weeks.week_of = pd.to_datetime(weeks.week_of)
weeks.to_csv('./data/weeks.csv',header=True, index=False)

print(f'Done in {time.time() - timer} seconds')


