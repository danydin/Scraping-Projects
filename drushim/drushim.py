from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import datetime, time, csv

current_time = datetime.datetime.now()
formatted_time = current_time.strftime("%d.%m %H;%M")
file_name = f"drushim {formatted_time}.csv"

url = "https://www.drushim.co.il/jobs/cat5/?experience=2&ssaen=3"

def load_more_btn():
    web.find_element(By.CSS_SELECTOR, ".load_jobs_btn").click()

header = ["Title", "Company", "Job description", "Requirements", "Categories","Link"]
jobs_rows = []

def write_csv(file, rows):
    with open(file, "w", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        writer.writerows(rows)

driver_path = "/opt/homebrew/bin/chromedriver"
opt = webdriver.ChromeOptions()
# opt.add_argument("--headless")
web = webdriver.Chrome(service=Service(driver_path), options=opt)
web.implicitly_wait(10)

web.get(url)

num = 1
print("\n started scraping... \n")
while True:
    try:
        print(f"div.jobList_vacancy:nth-child({num})")
        box = web.find_element(By.CSS_SELECTOR, f"div.jobList_vacancy:nth-child({num}) > div:nth-child(1) > div")
        divs = box.find_elements(By.TAG_NAME, 'div')
        title = divs[2].text
        company = divs[15].text
        # click on + לצפייה בפרטי המשרה
        divs[-8].click() 
        # gather all the divs again in the updated html after clicking the + button
        updated_divs = web.find_element(By.CSS_SELECTOR, f"div.jobList_vacancy:nth-child({num}) > div:nth-child(1) > div").find_elements(By.TAG_NAME, 'div')
        for description in updated_divs:
            text = description.text
            if "תיאור משרה" in text:
                job_desc = text.replace("\n", " ")
            if "דרישות התפקיד" in text:
                req = text.replace("\n", " ")
        box1 = box.find_elements(By.TAG_NAME, "a")
        box2 = box.find_elements(By.TAG_NAME, "tbody")
        box2 = [b.text for b in box2]
        categories = box2[0].replace("\n", " & ")
        link = box1[3].get_attribute("href")
        jobs_rows.append((title, company, job_desc, req, categories,link))
        # if want to limit results
        # if num==5:
        #     break
        num+=1
    except Exception as e:
        if "no such element: Unable to locate element:" in str(e):
            print('no more items - clickling on load more button')
            load_more_btn()
        elif "index out of range" in str(e):
                print('advertisment skip 1 div')
                num+=1
        else:
            print(e)
            print(f"\n\nFinished scraping successfully {num-1} listings")
            break
write_csv(file_name, jobs_rows)
