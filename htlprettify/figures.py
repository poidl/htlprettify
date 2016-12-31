#!/bin/python
# pylint: disable=C0103

"""Check that there is an *.svg for each *.pdf. Insert a (temporary)
   dummy *.png for *.pdf in tex file, to play nice with htlatex."""

import os
import glob
import shutil


def pdf2pngQuirk(path):
    """Check that there is an *.svg for each *.pdf. Insert a (temporary)
   dummy *.png for *.pdf in tex file, to play nice with htlatex."""
    listing = glob.glob(path + '/figures/*.pdf')
    for fname in listing:
        svgname = fname.replace('.pdf', '.svg')
        if not os.path.isfile(svgname):
            raise Exception('There is no file \"' +
                            os.path.basename(svgname) + '\"')
        # create a dummy *.png file
        shutil.copyfile(os.path.dirname(__file__) +
                        '/data/dummy.png', fname.replace('.pdf', '.png'))

    fin = open(path + "/main.tex", 'r')
    fout = open(path + "/tmp.tex", 'w')
    for line in fin:
        if '\\includegraphics' in line:
            fout.write(line.replace('.pdf', '.png'))
            continue
        fout.write(line)
    shutil.move(path + "/tmp.tex", path + "/main.tex")


def png2svgQuirk(path):
    """Replace dummy *.png with *.svg"""
    fin = open(path + "/main.html", 'r')
    fout = open(path + "/tmp.html", 'w')
    for line in fin:
        # TODO: use html parser here
        if 'src=' in line:
            fout.write(line.replace('.png', '.svg'))
            continue
        fout.write(line)
    shutil.move(path + "/tmp.html", path + "/main.html")
