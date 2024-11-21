
"""Load Library List, Print without formatting"""

import os
import re
import sys
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import chromedriver_autoinstaller
from pyvirtualdisplay import Display

def print_library_list():

    outfile = re.sub(os.path.basename(__file__), "raw_html.txt", os.path.abspath(__file__))

    with open(outfile, "r") as outfile:
        html_str = outfile.read()

    book_list_all = set()
    book_list_csv = set()
    book_list_csv.add("Title,Due Date")

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
        book_list_csv.add(
            f'{title_str}<p style="font-weight: bold; color: red;">{overdue_flag}</p>,{date_str}')

    book_list_all = sorted(book_list_all)

    outfile_name = re.sub(os.path.basename(__file__), "output.txt", os.path.abspath(__file__))

    with open(outfile_name, "w") as outfile:
        for book_info in book_list_all:
            print(book_info)
            outfile.write(f"{book_info}\n")

    with open(outfile_name.replace(".txt", ".csv") , "w") as outfile:
        for book_info in book_list_csv:
            outfile.write(f"<{book_info}\n")

    # os.system(f"code {outfile_name}")


def get_library_data(renew_all=False):

    display = Display(visible=0, size=(1800, 1200))  
    display.start()

    # change directory to the location of this file
    os.chdir(os.path.dirname(__file__))
             
    id_list = ("903675", "902232", "6596")

    options = Options()
    
    browser = webdriver.Chrome(options=options)

    browser.set_window_size(1800, 1200)
    html_str = ""

    for id in id_list:

        browser.get('https://hamb.agverso.com/login?cid=hamb&lid=HAMB')

        WebDriverWait(browser, 100.0, 2.0).until(
            EC.presence_of_element_located((By.ID, "username"))).send_keys(id)

        WebDriverWait(browser, 100.0, 2.0).until(
            EC.presence_of_element_located((By.ID, "password"))).send_keys("library"+Keys.ENTER)
        
        time.sleep(1)

        WebDriverWait(browser, 100.0, 2.0).until(EC.presence_of_element_located(
            (By.CLASS_NAME, "fa-angle-down"))).click()

        WebDriverWait(browser, 100.0, 2.0).until(
            EC.presence_of_element_located((By.XPATH, "//a[text()='Items Out ']"))).click()
        
        renew_all_button = WebDriverWait(browser, 100.0, 2.0).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//button[@aria-label='Renew All']")))

        if renew_all:
            renew_all_button.click()

            WebDriverWait(browser, 100.0, 2.0).until(
                EC.presence_of_element_located((By.XPATH, "//button[@aria-label='OK']"))).click()

        WebDriverWait(browser, 100.0, 2.0).until(EC.presence_of_element_located(
            (By.CLASS_NAME, "fa-angle-down"))).click()
        
        html_str = html_str + browser.page_source

        WebDriverWait(browser, 100.0, 2.0).until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[contains(text(), 'Logout')]"))).click()

        WebDriverWait(browser, 100.0, 2.0).until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[text()='Please Login ']" ))).click()
        
    outfile = re.sub(os.path.basename(__file__), "raw_html.txt", os.path.abspath(__file__))

    with open(outfile, "w") as outfile:
        outfile.write(html_str)


if len(sys.argv) >= 2 and sys.argv[1] in ("-r", "--renew-all"):
    get_library_data(True)        
else:
    get_library_data()
    
print_library_list()
