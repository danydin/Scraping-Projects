from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from time import sleep
import os, io, datetime

current_time = datetime.datetime.now()
formatted_time = current_time.strftime("%d.%m %H;%M")
file_name = f'drushim {formatted_time}.csv'


url = 'https://www.drushim.co.il/jobs/cat6/?experience=5&ssaen=3'


def box_css_selector(num):
    return f"div.jobList_vacancy:nth-child({num}) > div:nth-child(1) > div"

def more():
    web.find_element(By.CSS_SELECTOR, next_button).click()

next_button = '.load_jobs_btn'

def write_csv(file, column, row):
    csv1 = open(file, 'a', encoding='utf-8')
    csv1.write(column)
    csv1.write("\n")
    csv1.write(row)

driver_path = '/opt/homebrew/bin/chromedriver'
opt = webdriver.FirefoxOptions()
opt.add_argument("--headless")
web = webdriver.Firefox(service=Service(driver_path),options=opt)
web.implicitly_wait(10)

web.get(url)

num = 1
print('\nstarted scraiping...\n')
while True:
    try:
        try:
            box = web.find_element(By.CSS_SELECTOR, box_css_selector(num))
        except:
            try:
                more()
                box = web.find_element(By.CSS_SELECTOR, box_css_selector(num))
            except:
                print(f'\n\nFinished scraping sucessfully {num-1} listings')
                web.close()
                break

        box = box.find_elements(By.TAG_NAME, 'div')
        box[-8].click()
        title_1 = box[2].text
        cat1 = box[15].text.replace("\n", "")
        title_2 = box[13].text.replace("\n", "")
        box = web.find_element(By.CSS_SELECTOR, box_css_selector(num))
        divs = box.find_elements(By.TAG_NAME, 'div')
        for description in divs:
            text = description.text
            if 'תיאור משרה' in text:
                job_desc = text.replace('\n', '').replace(',', ".")
            if 'דרישות התפקיד' in text:
                req = text.replace('\n', '').replace(',', ".")
            
        box = web.find_element(By.CSS_SELECTOR, box_css_selector(num))
        box1 = box.find_elements(By.TAG_NAME, 'a')
        box2 = box.find_elements(By.TAG_NAME, 'tbody')
        box2 = [b.text for b in box2]
        catagory = box2[0].replace("\n", ' & ')
        link = box1[3].get_attribute('href')
        print(f"Title 1 : {title_1} \n&&\n Title 2 : {title_2} \n&&\n job desc: {job_desc} \n&&\n {req}")
        head= "Title 1,cat 1,Title 2, Job description, Requirments,Link, catagories"
        line = f'{title_1},{cat1},{title_2},{job_desc},{req},{link},{catagory}'
        num += 1
    except Exception as eee:
        print(eee)
        num += 1
        continue

    write_csv(file_name,head,line)


        #sleep(1)

