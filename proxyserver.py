import os
import csv
import time
import threading
import queue
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# url = "https://free-proxy-list.net/"
# driver.get(url)
# driver.maximize_window()
# # driver.execute_script(
# #     "window.scrollTo(0, document.documentElement.scrollHeight);")
# # time.sleep(2)

# # Click on the modal link
# modal = driver.find_element(
#     By.XPATH, '/html/body/section[1]/div/div[1]/ul/li[5]/a')
# modal.send_keys(Keys.RETURN)
# time.sleep(4)

# # Retrieve proxy values
# proxy_list = driver.find_element(
#     By.XPATH, '/html/body/div[1]/div/div/div[2]/textarea')
# proxy_values = proxy_list.text.split('\n')

# # Open the CSV file in append mode
# with open('rawproxies.csv', 'a', newline='') as file:
#     writer = csv.writer(file)

#     # Write data to the file
#     for proxy in proxy_values:
#         writer.writerow([proxy])

# # The file is automatically closed outside the 'with' block

# driver.quit()

# q = queue.Queue()
# lock = threading.Lock()

# with open("rawproxies.csv", "r") as f:
#     proxies = f.read().split("\n")
#     for p in proxies:
#         q.put(p)


def check_proxies():
    global q
    while not q.empty():
        proxy = q.get()
        try:
            res = requests.get("http://ipinfo.io/json",
                               proxies={"http": proxy,
                                        "https": proxy})
        except:
            continue
        if res.status_code == 200:
            print(proxy)
            with lock:
                with open('validproxies.csv', mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([proxy])


for _ in range(10):
    threading.Thread(target=check_proxies).start()


print("Completed")
import queue
import requests
import threading
import csv
q = queue.Queue()
lock = threading.Lock()

with open("rawproxies.csv", "r") as f:
    proxies = f.read().split("\n")
    for p in proxies:
        q.put(p)


def check_proxies():
    global q
    while not q.empty():
        proxy = q.get()
        try:
            res = requests.get("http://ipinfo.io/json",
                               proxies={"http": proxy,
                                        "https": proxy})
        except:
            continue
        if res.status_code == 200:
            print(proxy)
            with lock:
                with open('validproxies.csv', mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([proxy])


for _ in range(10):
    threading.Thread(target=check_proxies).start()

print("Completed")
