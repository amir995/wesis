import re
import time
import undetected_chromedriver as uc
from numpy.lib.utils import source
from selenium.webdriver.common.by import By
from seleniumbase import Driver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import pickle
import os
import re
import random
from pathlib import Path
import pandas as pd
import csv
from selenium.webdriver.common.by import By


def write_to_file(file_name, new_data):
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)

        for row in new_data:
            writer.writerow(row)
    print("written to file")





directory = Path("downloaded_files")
if not directory.is_dir():
    driver_creation = Driver(uc=True, guest_mode=True, disable_cookies=True, headless= True)
else:
    pass

# Start undetected ChromeDriver
options = uc.ChromeOptions()
#options.add_argument("--headless")  # Run in headless mode (optional)
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0",
    "Mozilla/5.0 (Windows NT 6.1; rv:61.0) Gecko/20100101 Firefox/61.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
]

# Select a random User-Agent
random_user_agent = random.choice(user_agents)

options.add_argument(f"--user-agent={random_user_agent}")
options.add_argument("--disable-extensions")
options.add_argument("--disable-popup-blocking")
options.add_argument("--accept-language=en-US,en;q=0.9")
options.add_argument("--accept-encoding=gzip, deflate, br")
options.add_argument("--connection=keep-alive")
options.add_argument('--headless')






# Initialize the driver
driver = uc.Chrome(options=options)



url = "https://www.wesis.org/indicators/1"
driver.get(url)
driver.maximize_window()
time.sleep(1)
user_id = "alupotol794@gmail.com"
pass_word = "018340.abcA"
id_box = driver.find_element(By.ID,("session_email")).send_keys(user_id)
pass_box = driver.find_element(By.ID,("session_password")).send_keys(pass_word + Keys.ENTER)
time.sleep(1)


breadcrumb_links = driver.find_element(By.CSS_SELECTOR, 'nav[aria-label="breadcrumb"]')

breadcrumb_data = breadcrumb_links.text.split("\n")
breadcrumb_data_len = (len(breadcrumb_data))

if breadcrumb_data_len ==6 and "attainment" in breadcrumb_links.text.lower() :
    social_policies = breadcrumb_data[1]
    attainment = breadcrumb_data[3]
    sub_category = breadcrumb_data[4]
    indicator = breadcrumb_data[5]
else:
    try:
        social_policies = breadcrumb_data[1]
        attainment = breadcrumb_data[2]
        sub_category = breadcrumb_data[3]
        indicator = breadcrumb_data[breadcrumb_data_len-1]
    except:
        social_policies = breadcrumb_data[1]
        indicator = breadcrumb_data[breadcrumb_data_len-1]
        attainment = ""
        sub_category = ""
'''
try:
    social_policies = breadcrumb_data[1]
    attainment = breadcrumb_data[3]
    sub_category = breadcrumb_data[4]
    indicator = breadcrumb_data[5] or None
except IndexError:
    indicator= None
'''

a = driver.find_elements(By.CLASS_NAME,"info-card-content")

data = ""
for x in a:
    if "Technical name" in x.text:
        data = x.text
        data = str(data)

lines = data.split("\n")

# Extract values
technical_name = next(line.split(":")[1].strip() for line in lines if line.startswith("Technical name:"))
scale = next(line.split(":")[1].strip() for line in lines if line.startswith("Scale:"))
description_index = lines.index("Description:") + 1
description_raw = str("\n".join(lines[description_index:]).strip())
description = re.sub(r"Related Indicators:.*", "", description_raw, flags=re.DOTALL)



match = re.search(r"Related Indicators:(.*)", description_raw, re.DOTALL)
related_indicators = ""
if match:
    result = match.group(1).strip()
    related_indicators = str(result)
#
# print("# url link is >> " + url)
# print(social_policies)
# print(attainment)
# print(sub_category)
# print(indicator)
# print(technical_name)
# print(scale)
# print(description)
# print(related_indicators)

tab = driver.find_element(By.ID, 'mdc-tab-2')
tab.click()

coding_rules = driver.find_element(By.XPATH, "//div[@class='info-card-content']//p")
coding_rules = coding_rules.text if coding_rules.text else None

tab = driver.find_element(By.ID, 'mdc-tab-3')
tab.click()
citation = driver.find_element(By.XPATH, "//*[@id='info-tabs']/div[4]/div/div").text

tab = driver.find_element(By.ID, 'mdc-tab-4')
tab.click()
li_elements = driver.find_elements(By.XPATH, "//*[@id='info-tabs']/div[5]/div//ul//li")

li_item_list = []
for li in li_elements:
    a_tag = li.find_element(By.TAG_NAME, "a") if len(li.find_elements(By.TAG_NAME, "a")) > 0 else None

    if a_tag:
        li_item_list.append(f"{li.text}{a_tag.text}")
    else:
        li_item_list.append(f"{li.text}")


tab = driver.find_element(By.ID, 'mdc-tab-5')
tab.click()
source_li_elements = driver.find_elements(By.XPATH, "//*[@id='info-tabs']/div[6]/div//ul//li")

source_li_item_list = []
for li in source_li_elements:
    a_tag = li.find_element(By.TAG_NAME, "a") if len(li.find_elements(By.TAG_NAME, "a")) > 0 else None

    if a_tag:
        source_li_item_list.append(f"{li.text}{a_tag.text}")
    else:
        source_li_item_list.append(f"{li.text}")


tab = driver.find_element(By.ID, 'mdc-tab-6')
tab.click()

misc_content = driver.find_element(By.XPATH, "//div[@class='mdc-card info info--active']//div[@class='info-card-content']")
misc = misc_content.text  if misc_content.text  else None



new_data = {
    "Social Policies": [social_policies],
    "Attainment": [attainment],
    "Sub Sub-category": [sub_category],
    "Indicator": [indicator],
    "Technical name": [technical_name],
    "Description": [description],
    "Related Indicators": [related_indicators],
    "Coding Rules": [coding_rules],
    "Citation": [citation],
    "Related Publications": '\n'.join(li_item_list),
    "Sources": '\n'.join(source_li_item_list),
    "Misc": misc
}

file_path = "data.csv"
df = pd.DataFrame(new_data)

df.to_csv(file_path, mode='a', index=False, header=False)
data = pd.read_csv(file_path)

time.sleep(3)

driver.close()
