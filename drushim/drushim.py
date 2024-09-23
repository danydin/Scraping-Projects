from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import datetime, csv, re, time

driver_path = "/opt/homebrew/bin/chromedriver"
opt = webdriver.ChromeOptions()
opt.add_argument("--headless")
web = webdriver.Chrome(service=Service(driver_path), options=opt)
web.implicitly_wait(10)

current_time = datetime.datetime.now()
formatted_time = current_time.strftime("%d.%m") #  %H_%M

url = "https://www.drushim.co.il/jobs/search/היברידי/?experience=1-2&ssaen=3"
web.get(url)
pattern = r'/search/([^/]+)/?'
regex_search = re.search(pattern, url)
if regex_search:
    # Extract the word between the slashes after the /search/ in the url below
    drushim_search_term = regex_search.group(1)
file_name = f"{drushim_search_term}-{formatted_time}.csv"

total_listings_text = web.find_element(By.CSS_SELECTOR, 'h2.display-36-24.primary--text').text
total_listings = re.findall(r'\d+',total_listings_text)[0]

current_ad = 1

header = ["Title", "Company", "Job description", "Requirements", "Categories","Link"]
jobs_rows = []

def write_csv(file, rows):
    with open(file, "w", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        writer.writerows(rows)

print(f"\n started scraping {total_listings} listings \n")

def load_more_btn():
    web.find_element(By.CSS_SELECTOR, ".load_jobs_btn").click()
    time.sleep(2)

while True:
    try:
        print(f"div.jobList_vacancy:nth-child({current_ad})")
        box = web.find_element(By.CSS_SELECTOR, f"div.jobList_vacancy:nth-child({current_ad}) > div:nth-child(1) > div")
        divs = box.find_elements(By.TAG_NAME, 'div')
        # find the div corresponding to the info you want to scrape
        # for div in divs:
        #     print(f'{div.get_attribute("innerHTML")}\n\n')
        title = divs[2].text
        company = divs[15].text
        # click on + לצפייה בפרטי המשרה
        divs[-8].click() 
        # gather all the divs again in the updated html after clicking the + button
        updated_divs = web.find_element(By.CSS_SELECTOR, f"div.jobList_vacancy:nth-child({current_ad}) > div:nth-child(1) > div").find_elements(By.TAG_NAME, 'div')
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
        current_ad+=1
        # break loop if completed scraping all listings
        if current_ad == int(total_listings)+1:
            break
    except Exception as e:
        if "no such element: Unable to locate element:" in str(e):
            print('no more items - clickling on load more button')
            load_more_btn()
        elif "index out of range" in str(e):
                print('advertisement div - skipping 1 div')
                current_ad+=1
                continue
        elif "element click intercepted" in str(e):
            continue
        else:
            print(e)
            break

write_csv(file_name, jobs_rows)
print(f"\nFinished scraping successfully {current_ad-1} out of {total_listings} listings \n")
