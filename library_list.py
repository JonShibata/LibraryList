
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

    outfile = re.sub(os.path.basename(__file__),
                     "raw_html.txt", os.path.abspath(__file__))

    with open(outfile, "r") as outfile:
        html_str = outfile.read()

    book_list_html = set()

    book_list = re.findall(
        'Title: .*?<.*?-c[0-9]{2,}="">(.*?)<.*?Due Date:.*?<.*?-c[0-9]{2,}="">([0-9]{1,2}/[0-9]{1,2})/',
        html_str, flags=re.DOTALL)

    for book_info in book_list:
        title_str = book_info[0].replace("&amp;", "&")
        date_items = book_info[1].split("/")

        due_year = datetime.now().year
        if datetime.now().month == 12 and int(date_items[0]) == 1:
            due_year += 1

        date_str = f"{due_year}/{date_items[0]:0>2}/{date_items[1]:0>2}"
        book_date = datetime(due_year, int(date_items[0]), int(date_items[1]))

        if datetime.now() > book_date:
            overdue_string_html = '<p style="font-weight: bold; color: red;"> *** OVERDUE *** </p>'
        else:
            overdue_string_html = ""

        book_list_html.add(f"{overdue_string_html}{title_str}*^*{date_str}")

    book_list_html = sorted(book_list_html)

    outfile_name = re.sub(os.path.basename(__file__),
                          "output.txt", os.path.abspath(__file__))

    with open(outfile_name, "w") as outfile:
        for book_info in book_list_html:
            book_info = book_info.replace("*^*", " - ").replace(
                "<p style=\"font-weight: bold; color: red;\"> *** OVERDUE *** </p>",
                " *** OVERDUE *** ")

            print(book_info)
            outfile.write(f"{book_info}\n")

    with open(outfile_name.replace(".txt", "_html.txt"), "w") as outfile:
        for book_info in book_list_html:
            outfile.write(f"{book_info}\n")

    # os.system(f"code {outfile_name}")


def get_library_data(renew_all=False):

    display = Display(visible=0, size=(1800, 1200))
    display.start()

    # change directory to the location of this file
    os.chdir(os.path.dirname(__file__))

    id_dict = {}
    id_dict[os.environ["USERNAME1"]] = os.environ["PASSWORD1"]
    id_dict[os.environ["USERNAME2"]] = os.environ["PASSWORD2"]
    id_dict[os.environ["USERNAME3"]] = os.environ["PASSWORD3"]

    options = Options()

    browser = webdriver.Chrome(options=options)

    browser.set_window_size(1800, 1200)
    html_str = ""

    for id in id_dict.keys():

        browser.get('https://hamb.agverso.com/login?cid=hamb&lid=HAMB')

        WebDriverWait(browser, 100.0, 2.0).until(
            EC.presence_of_element_located((By.ID, "username"))).send_keys(id)

        WebDriverWait(browser, 100.0, 2.0).until(
            EC.presence_of_element_located((By.ID, "password"))).send_keys(id_dict[id]+Keys.ENTER)

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
                (By.XPATH, "//a[text()='Please Login ']"))).click()

    outfile = re.sub(os.path.basename(__file__),
                     "raw_html.txt", os.path.abspath(__file__))

    with open(outfile, "w") as outfile:
        outfile.write(html_str)


if len(sys.argv) >= 2 and sys.argv[1] in ("-r", "--renew-all"):
    get_library_data(True)
else:
    get_library_data()

print_library_list()
