#!/bin/python
# pylint: disable=C0103

"""Check that there is an *.svg for each *.pdf. Insert a (temporary)
   dummy *.png for *.pdf in tex file, to play nice with htlatex."""

import os
import glob
import shutil
import re
from bs4 import BeautifulSoup
import myutils


# def pdf2pngQuirk(path, ):
#     """Check that there is an *.svg for each *.pdf. Insert a (temporary)
#    dummy *.png for *.pdf in tex file, to play nice with htlatex."""
#     listing = glob.glob(path + '/figures/*.pdf')
#     for fname in listing:
#         svgname = fname.replace('.pdf', '.svg')
#         if not os.path.isfile(svgname):
#             raise Exception('There is no file \"' +
#                             os.path.basename(svgname) + '\"')
#         # create a dummy *.png file
#         shutil.copyfile(os.path.dirname(__file__) +
#                         '/data/dummy.png', fname.replace('.pdf', '.png'))

#     fin = open(path + "/main.tex", 'r')
#     fout = open(path + "/tmp.tex", 'w')
#     for line in fin:
#         if '\\includegraphics' in line:
#             fout.write(line.replace('.pdf', '.png'))
#             continue
#         fout.write(line)
#     shutil.move(path + "/tmp.tex", path + "/main.tex")


def adjustFigPath(buildpath, figpath):
    """Check that there is an *.svg for each *.pdf. Insert a (temporary)
   dummy *.png for *.pdf in tex file, to play nice with htlatex."""
    #  temporary figure directory
    tmp = buildpath + '/figures'
    os.system('mkdir ' + tmp)
    listing = glob.glob(figpath + '/*.pdf')
    for fname in listing:
        svgname = fname.replace('.pdf', '.svg')
        if not os.path.isfile(svgname):
            raise Exception('There is no file \"' +
                            os.path.basename(svgname) + '\"')
        # move dummy *.png file to temporary figure directory
        newname = tmp + '/' + \
            os.path.basename(fname).replace('.pdf', '.png')
        shutil.copyfile(os.path.dirname(__file__) +
                        '/data/dummy.png', newname)

    fin = open(buildpath + "/main.tex", 'r')
    fout = open(buildpath + "/tmp.tex", 'w')
    for line in fin:
        if '\\graphicspath' in line:
            # no brackets, no SPACE
            a = re.finditer(r'[^{} ]*',
                            line.replace('\\graphicspath', '').replace('\n', ''))
            b = [m.group(0) for m in a]
            l = list(filter(None, b))
            # append temporary path
            l.append(tmp + '/')
            ml = ['{' + e + '}' for e in l]
            myline = '\\graphicspath{' + ''.join(ml) + '}'
            fout.write(line.replace(line, myline))
            continue
        if '\\includegraphics' in line:
            fout.write(line.replace('.pdf', '.png'))
            continue
        fout.write(line)
    shutil.move(buildpath + "/tmp.tex", buildpath + "/main.tex")


def move(figurepath, installimgpath_abs):
    """Move figures to installation path"""
    cp = myutils.Copier(figurepath, installimgpath_abs)
    listing = glob.glob(figurepath + '/*.svg')
    for fname in listing:
        cp.copy(os.path.basename(fname))


def png2svgSubstitution(buildpath, installimgpath):
    """Replace dummy * .png with *.svg"""

    f = open(buildpath + "/main.html")
    s = f.read()

    soup = BeautifulSoup(s, 'html.parser')

    sectitlelist = soup.find_all('img')
    ls = len(sectitlelist)
    for i in range(ls):
        l = sectitlelist[i]
        l['src'] = l['src'].replace('png', 'svg')

    html = str(soup)
    f = open(buildpath + "/main.html", "w")
    f.write(html)


def changeHtmlFigpath(buildpath, newpath):
    """Change html figure path"""

    f = open(buildpath + "/main.html")
    s = f.read()

    soup = BeautifulSoup(s, 'html.parser')

    sectitlelist = soup.find_all('img')
    ls = len(sectitlelist)
    for i in range(ls):
        l = sectitlelist[i]
        l['src'] = newpath + '/' + os.path.basename(l['src'])

    html = str(soup)
    f = open(buildpath + "/main.html", "w")
    f.write(html)

    #     fin = open(buildpath + "/main.html", 'r')
    # fout = open(buildpath + "/tmp.html", 'w')
    # for line in fin:
    #     # TODO: use html parser here
    #     if 'src=' in line:
    #         m = re.sub(r'{.*}')
    #         fout.write(line.replace('.png', '.svg'))
    #         continue
    #     fout.write(line)
    # shutil.move(buildpath + "/tmp.html", buildpath + "/main.html")
