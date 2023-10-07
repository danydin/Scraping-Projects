import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests

url = 'https://www.drushim.co.il/jobs/search/משרה%20היברידית/?ssaen=1'

options = Options()
options.headless = True
driver_path = '/opt/homebrew/bin/chromedriver'
driver = webdriver.Chrome(service=Service(driver_path), options=options)
driver.get(url)
resultsLimit = 4

# while True:
for i in range(resultsLimit): 
    try:
        load_more_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.load_jobs_btn')))
        load_more_button.click()
        time.sleep(5)
    except:
        break

elements = driver.find_elements(By.CSS_SELECTOR, 'p.display-18.view-on-submit.mb-0')
for element in elements[:resultsLimit]:
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});", element)
    time.sleep(3)
    element.click()

soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

titles = []
descriptions = []
for job in soup.select('.job-item-main')[:resultsLimit]:
    try:
        title = job.select_one('.job-url').text.strip()
        description = job.select_one('.layout.job-details-box.vacancyFullDetails.wrap').text.strip()
        titles.append(title)
        descriptions.append(description)
        print(titles)
# if AttributeError: 'NoneType' object has no attribute 'text'
    except AttributeError:
        # Handle the error here
        title = job.select_one('.job-url').text.strip()
        description = 'Missing Desc'
        titles.append(title)
        descriptions.append(description)
        print('Missing Desc')

data = {'Title': titles, 'Description': descriptions}
df = pd.DataFrame(data)
df.to_csv('drushim_jobs.csv', index=False)