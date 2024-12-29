import re
import time
import undetected_chromedriver as uc
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






# Initialize the driver
driver = uc.Chrome(options=options)



url = "https://www.wesis.org/indicators/667"
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

social_policies = breadcrumb_data[1]
attainment = breadcrumb_data[3]
sub_category = breadcrumb_data[4]
indicator = breadcrumb_data[5]


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

print("# url link is >> " + url)
print(social_policies)
print(attainment)
print(sub_category)
print(indicator)
print(technical_name)
print(scale)
print(description)
print(related_indicators)


new_data = {
            "Social Policies Attainment": [social_policies],
            "Attainment": [attainment],
            "Sub Sub-category":[sub_category],
            "Indicaticator":[indicator],
            "Tecnicle name":[technical_name],
            "Description":[description],
            "Related Indicators":[related_indicators]
        }

file_path = "data.csv"
df = pd.DataFrame(new_data)

df.to_csv(file_path, mode='a', index=False, header=False)
data = pd.read_csv(file_path)

time.sleep(3)

driver.close()
'''

url = "https://www.wesis.org/indicators/663"
id = driver.find_element(by,"session_email").send
pas = driver.find_element(by,"session_password")
time.sleep(200)
driver.quit()
'''