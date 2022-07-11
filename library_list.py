

"""Load Library List, Print without formatting"""

import re

from tkinter.filedialog import askopenfilenames


def print_library_list():

    html_files = askopenfilenames(title="Select Library Lists",
                                 filetypes=[(".HTML", ".html")])

    book_list_all = []

    for html_file in html_files:

        with open(html_file) as html_str:
            book_list = re.findall("{}{}{}{}".format(
                '<div _ngcontent-spc-c521="" class="ng-star-inserted">',
                ' Title: <b _ngcontent-spc-c521="">',
                '(.*?)',
                '</b>'),
                html_str.read(), flags=re.DOTALL)

        for book_title in book_list:
            book_list_all.append(book_title)


    book_list_all.sort()

    for book_title in book_list_all:
        print(book_title)


print_library_list()
