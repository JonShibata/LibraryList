
"""Load Library List, Print without formatting"""

import os
import subprocess
import re


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys



def print_library_list(html_str):


    book_list_all = set()

    book_list = re.findall("{}".format(
        'Title: .*?<.*?-c521="">(.*?)<.*?DateDue:.*?<.*?-c521="">([0-9]{1,2}/[0-9]{1,2})/'),
        html_str, flags=re.DOTALL)

    for book_info in book_list:
        title_str = book_info[0].replace("&amp;", "&")
        book_list_all.add("{}-{}".format(book_info[1], title_str))


    book_list_all = sorted(book_list_all)
    
    outfile = re.sub(os.path.basename(__file__), "output.txt", os.path.abspath(__file__))

    with open(outfile, "w") as outfile:
        for book_title in book_list_all:
            print(book_title)
            outfile.write("{}\n".format(book_title))

    outfile = re.sub(os.path.basename(__file__), "raw_html.txt", os.path.abspath(__file__))

    with open(outfile, "w") as outfile:
        outfile.write(html_str)


    # subprocess.run("gedit {}".format(outfile))





def get_library_data():

    id_list = ("903675", "902232", "6596")


    browser = webdriver.Chrome()
    browser.set_window_size(1800, 1200)
    html_str = ""

    for id in id_list:

        browser.get('https://hamb.agverso.com/login?cid=hamb&lid=HAMB')

        WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(id)
        
        password_box = browser.find_element(By.ID, "password")
        password_box.send_keys("library")
        password_box.send_keys(Keys.RETURN) 

        WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.CLASS_NAME, "fa-angle-down"))).click()

        WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.ID, "itemsOut"))).click()

        WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.CLASS_NAME, "mx-auto")))

        html_str = html_str + browser.page_source

        WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.CLASS_NAME, "fa-angle-down"))).click()

        WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.ID, "logOut"))).click()

    return (html_str)



print_library_list(get_library_data())

