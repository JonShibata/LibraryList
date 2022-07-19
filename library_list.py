
"""Load Library List, Print without formatting"""

import os
import subprocess
import re

from tkinter.filedialog import askopenfilenames


def print_library_list():

    html_files = askopenfilenames(title="Select Library Lists",
                                 filetypes=[(".HTML", ".html")])

    book_list_all = set()

    for html_file in html_files:

        with open(html_file) as html_str:
            book_list = re.findall("{}".format(
                'Title: .*?<.*?-c521="">(.*?)<'),
                html_str.read(), flags=re.DOTALL)

        for book_title in book_list:
            book_list_all.add(book_title)


    book_list_all = sorted(book_list_all)

    outfile = re.sub(os.path.basename(__file__), "output.txt", os.path.abspath(__file__))

    with open(outfile, "w") as outfile:
        for book_title in book_list_all:
            print(book_title)
            outfile.write("{}\n".format(book_title))

    # subprocess.run("gedit {}".format(outfile))

print_library_list()
