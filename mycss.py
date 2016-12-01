#!/bin/python
# pylint: disable=C0103

"""CSS modifications"""

import shutil
from bs4 import BeautifulSoup


def figs(path):
    """Inject a style attribute to <img> and their <p> parents"""
    # TODO: Here we are injecting style attributes to *.html. Is it better to
    # define a new css class and reference that from *.html instead?

    f = open(path + "/main.html")
    s = f.read()

    soup = BeautifulSoup(s, 'html.parser')

    sectitlelist = soup.find_all('img')
    ls = len(sectitlelist)
    for i in range(ls):
        l = sectitlelist[i]
        l['style'] = "width: 100%; max-width: 800px;"
        l.parent['style'] = "text-align:center"

    html = soup.prettify()
    f = open(path + "/main.html", "w")
    f.write(html)


def fonts(path):
    """Insert default font family in .css file."""
    fin = open(path + "/main.css", 'r')
    fout = open(path + "/tmp.css", 'w')

    s = "* {\n  font-family: 'Droid Sans', Arial, Verdana, sans-serif;\n}"
    fout.write(s)
    for line in fin:
        fout.write(line)
    shutil.move(path + "/tmp.css", path + "/main.css")


def body(path):
    """Set a body style max-width suitable for large monitors."""
    f = open(path + "/main.html")
    s = f.read()

    soup = BeautifulSoup(s, 'html.parser')

    soup.body[
        'style'] = "font-size: 100%; width=100%; max-width: 800px; padding: 1em; margin: auto;"
    html = soup.prettify()
    f = open(path + "/main.html", "w")
    f.write(html)
