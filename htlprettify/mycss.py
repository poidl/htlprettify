#!/bin/python
# pylint: disable=C0103

"""CSS modifications"""

import shutil
import re
from bs4 import BeautifulSoup


def getFigSize(buildpath):
    fin = open(buildpath + "/main.tex", 'r')
    for line in fin:
        # if '\\graphicspath' in line:
        #     # no brackets, no SPACE
        #     # a = re.finditer(r'[^{} ]*',
        #     #                 line.replace('\\graphicspath', '').replace('\n', ''))
        #     # b = [m.group(0) for m in a]
        #     # l = list(filter(None, b))
        #     # # append temporary path
        #     # l.append('figures/')
        #     l = ['figures/']
        #     ml = ['{' + e + '}' for e in l]
        #     myline = '\\graphicspath{' + ''.join(ml) + '}'
        #     fout.write(line.replace(line, myline))
        #     continue
        # \includegraphics[width = 0.5\textwidth]{met_t2micro.png}
        if '\\includegraphics' in line:
            if not '\\textwidth' in line:
                raise Exception(
                    "There is no 'width = *\\textwidth' in the includegraphics command, figure sizing won't work.")
            m = re.search('[0-9]\.[0-9]*(?=.*textwidth)', line)
            if m:
                sz = m.group(0)
                return sz
            else:
                raise Exception("Could not retrieve figure size from latex.")

# fout.write(line.replace('.pdf', '.png'))
# continue


def figs(path):
    """Inject a style attribute to <img> and their <p> parents"""
    # TODO: Here we are injecting style attributes to *.html. Is it better to
    # define a new css class and reference that from *.html instead?
    sz = getFigSize(path)

    f = open(path + "/main.html")
    s = f.read()

    soup = BeautifulSoup(s, 'html.parser')

    sectitlelist = soup.find_all('img')
    ls = len(sectitlelist)
    for i in range(ls):
        l = sectitlelist[i]
        l['style'] = "width: " + \
            str(round(float(sz) * 100)) + "%; max-width: 800px;"
        l.parent['style'] = "text-align:center"

    html = str(soup)
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
    html = str(soup)
    f = open(path + "/main.html", "w")
    f.write(html)


def backtotop(path):
    """Back-to-top button for long single-pages."""
    fin = open(path + "/main.css", 'r')
    fout = open(path + "/tmp.css", 'w')

    s = """a.back-to-top {
    background-color: blue;
    opacity: 0.8;
    border: none;
    color: white;
	border-radius: 12px;
    padding: 10px 15px;
    text-align: center;
    text-decoration: none;
    display: none;
    font-size: 16px;
	z-index: 999;
}
"""

    for line in fin:
        fout.write(line)
    fout.write(s)
    shutil.move(path + "/tmp.css", path + "/main.css")
