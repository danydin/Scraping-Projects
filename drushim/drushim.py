from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from time import sleep
import os, io, datetime

current_time = datetime.datetime.now()
formatted_time = current_time.strftime("%d.%m %H;%M")
file_name = f"drushim {formatted_time}.csv"


url = "https://www.drushim.co.il/jobs/cat5/?experience=2&ssaen=3"


def box_css_selector(num):
    return f"div.jobList_vacancy:nth-child({num}) > div:nth-child(1) > div"


def load_more_btn():
    web.find_element(By.CSS_SELECTOR, ".load_jobs_btn").click()


def write_csv(file, column, row):
    with open(file, "a", encoding="utf-8") as csv_file:
        csv_file.write(column)
        csv_file.write("\n")
        csv_file.write(row)


driver_path = "/opt/homebrew/bin/chromedriver"
opt = webdriver.ChromeOptions()
# opt.add_argument("--headless")
web = webdriver.Chrome(service=Service(driver_path), options=opt)
web.implicitly_wait(10)

web.get(url)

num = 1
print("\n started scraiping... \n")
while True:
    try:
        try:
            box = web.find_element(By.CSS_SELECTOR, box_css_selector(num))
        except:
            try:
                load_more_btn()
                box = web.find_element(By.CSS_SELECTOR, box_css_selector(num))
            except:
                print(f"\n\nFinished scraping sucessfully {num-1} listings")
                web.close()
                break

        box = box.find_elements(By.TAG_NAME, "div")
        # # click on + לצפייה בפרטי המשרה
        # box[-8].click()
        title = box[2].text
        company = box[15].text
        # issue printing it without cling the box first
        # title_2 = box[13].text.replace("\n", "")
        # print(title_2)
        # for description in box:
        #     text = description.text
        #     if "תיאור משרה" in text:
        #         job_desc = text.replace("\n", "").replace(",", ".")
        #     if "דרישות התפקיד" in text:
        #         req = text.replace("\n", "").replace(",", ".")

        # box = web.find_element(By.CSS_SELECTOR, box_css_selector(num))
        # box1 = box.find_elements(By.TAG_NAME, "a")
        # box2 = box.find_elements(By.TAG_NAME, "tbody")
        # box2 = [b.text for b in box2]
        # catagory = box2[0].replace("\n", " & ")
        # link = box1[3].get_attribute("href")
        print(
            f"/n Title 1 : {title} \n Comapny: {company}"
        )
        head = (
            "Title 1, Company, Title 2, Job description, Requirments, Link, Categories"
        )
        # line = f"{title},{company},{title_2},{job_desc},{req},{link},{catagory}"
        line = f"{title},{company}"
        num += 1
        print(num)
        write_csv(file_name, head, line)
    except Exception as eee:
        print(eee)
        num += 1
        continue
