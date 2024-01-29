
"""Load Library List, Print without formatting"""

import os
import subprocess
import re
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def print_library_list():

    outfile = re.sub(os.path.basename(__file__), "raw_html.txt", os.path.abspath(__file__))

    with open(outfile, "r") as outfile:
        html_str = outfile.read()

    book_list_all = set()

    book_list = re.findall(
        'Title: .*?<.*?-c[0-9]{2,}="">(.*?)<.*?Due Date:.*?<.*?-c[0-9]{2,}="">([0-9]{1,2}/[0-9]{1,2})/',
        html_str, flags=re.DOTALL)

    for book_info in book_list:
        title_str = book_info[0].replace("&amp;", "&")
        date_items = book_info[1].split("/")
        date_str = f"{date_items[0]:0>2}/{date_items[1]:0>2}"

        overdue_flag = " *** OVERDUE *** "
        book_date = datetime(datetime.now().year, int(date_items[0]), int(date_items[1]))
        if datetime.now() < book_date:
            overdue_flag = ""

        book_list_all.add(f"{overdue_flag}{title_str} - {date_str}")

    book_list_all = sorted(book_list_all)

    outfile_name = re.sub(os.path.basename(__file__), "output.txt", os.path.abspath(__file__))

    with open(outfile_name, "w") as outfile:
        for book_title in book_list_all:
            print(book_title)
            outfile.write(f"{book_title}\n")

    os.system(f"code {outfile_name}")


def get_library_data():

    # change directory to the location of this file

    os.chdir(os.path.dirname(__file__))
             
    id_list = ("903675", "902232", "6596")

    options = Options()
    options.binary_location = "chrome-win64/chrome.exe"
    browser = webdriver.Chrome(options=options)

    browser.set_window_size(1800, 1200)
    html_str = ""

    for id in id_list:

        browser.get('https://hamb.agverso.com/login?cid=hamb&lid=HAMB')

        WebDriverWait(browser, 100.0, 2.0).until(
            EC.presence_of_element_located((By.ID, "username"))).send_keys(id)

        WebDriverWait(browser, 100.0, 2.0).until(
            EC.presence_of_element_located((By.ID, "password"))).send_keys("library"+Keys.ENTER)

        WebDriverWait(browser, 100.0, 2.0).until(EC.presence_of_element_located(
            (By.CLASS_NAME, "fa-angle-down"))).click()

        WebDriverWait(browser, 100.0, 2.0).until(
            EC.presence_of_element_located((By.XPATH, "//a[text()='Items Out ']"))).click()
        
        WebDriverWait(browser, 100.0, 2.0).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[@aria-label='Renew All']"))).click()

        WebDriverWait(browser, 100.0, 2.0).until(
            EC.presence_of_element_located((By.XPATH, "//button[@aria-label='OK']"))).click()

        WebDriverWait(browser, 100.0, 2.0).until(EC.presence_of_element_located(
            (By.CLASS_NAME, "fa-angle-down"))).click()
        
        html_str = html_str + browser.page_source

        WebDriverWait(browser, 100.0, 2.0).until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[contains(text(), 'Logout')]"))).click()

    outfile = re.sub(os.path.basename(__file__), "raw_html.txt", os.path.abspath(__file__))

    with open(outfile, "w") as outfile:
        outfile.write(html_str)


get_library_data()
print_library_list()
