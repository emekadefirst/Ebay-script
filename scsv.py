import csv
import time
import subprocess
import pandas as pd
from datetime import datetime
from tqdm import tqdm
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Run the other script as a subprocess
subprocess.run(["python", "proxyserver.py"])

# WEB DRIVER ACTIVATION
# options = Options()
# options.headless = True
# , options=options
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()))
print("RUNNING HEADLESS MODE-----")
url = "https://www.ebay.com/b/2018-Apple-MacBook-Air-Laptops/111422/bn_7114024041"
driver.get(url)
print("BROWSER OPENED------")
driver.maximize_window()
print("BROWSER WINDOW ON MAX SCREEN-------")

# Perform the loop 6 times
num_pg = 6  # Set the number of pages to scrape here

data = []
print("PROGRESS BAR IS STARTING-------")
# Create a progress bar for scraping pages
progress_bar_pages = tqdm(total=num_pg, desc='Scraping Pages', unit='page')
print("GETTING THE WEBPAGES AVAILABLE--------")
for i in range(num_pg):
    driver.get(
        f'https://www.ebay.com/b/2018-Apple-MacBook-Air-Laptops/111422/bn_7114024041?rt=nc&_pgn={i + 1}')
    # Scroll to the bottom of the page
    driver.execute_script(
        "window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(2)  # Wait for the page to load, adjust sleep duration as needed

    # Scrape the content here
    items = driver.find_elements(By.CLASS_NAME, 's-item__wrapper')

    # Create a progress bar for scraping items
    progress_bar_items = tqdm(items, desc='Scraping Items', unit='item')

    for item in progress_bar_items:
        name_element = item.find_element(By.CLASS_NAME, 's-item__title')
        url_element = item.find_element(By.CLASS_NAME, 's-item__link')
        price_element = item.find_element(By.CLASS_NAME, 's-item__price')

        name = name_element.text
        url = url_element.get_attribute('href')
        price = price_element.text

        row = {
            'Name': name,
            'URL': url,
            'Price': price
        }

        data.append(row)

    # Close the progress bar for scraping items
    progress_bar_items.close()
    # Update the progress bar for scraping pages
    progress_bar_pages.update(1)

# Close the progress bar for scraping pages
progress_bar_pages.close()

driver.quit()

# Generate a unique ID for the CSV file name
now = datetime.now()
timestamp = now.strftime("%Y%m%d%H%M%S")
filename = f'data{timestamp}.csv'

# Save the data to a CSV file
keys = data[0].keys()
with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=keys)
    writer.writeheader()
    writer.writerows(data)

print("Data saved to CSV file:", filename)
