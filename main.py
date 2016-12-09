#!/bin/python
# pylint: disable=C0103

"""Post-process htlatex output"""

import shutil
import os
import utils
import figures
import mycss
import myhtml

# Root directory of latex project, containing latex source
path = '/home/stefan/Documents/bewerbungen/mfund'
# Build directory for latex and htlatex
tmpdir = 'build'
# Set an alternative document title and subtitle. Empty string defaults to (possibly
# too long) latex title.
title = 'Numerical Ocean/Weather Modeling Platform as a Service'
subtitle = 'Proposal for a feasibility study'
# Set an alternative document title in <head> (title for browser tabs). Empty string defaults to (possibly
# too long) latex title.
headtitle = 'Proposal mFUND'


# Create build directory and copy latex source files
if os.path.isdir(tmpdir):
    shutil.rmtree(tmpdir)
os.mkdir(tmpdir)
os.mkdir(tmpdir + '/nobackup')
cp = utils.Copier(path, tmpdir)
cp.copy('main.tex')
cp.copy('paper.bib')
cp.copy('model2-names.bst')
cp.copytree('figures')

# Assumes use of pdflatex, or more generally, that figures included in the
# latex source are PDFs. Furthermore assumes that for each PDF, an SVG of
# the same name is present (SVG is best for HTML?). Substitute them
# temporarily by PNGs, to avoid errors with latex and htlatex.

figures.pdf2pngQuirk(tmpdir)

# Latex first run
cmd = 'cd ' + tmpdir + '; latex -synctex=1 -output-directory=nobackup' \
    + ' -interaction=nonstopmode main.tex'
print(cmd)
os.system(cmd)

# Bibtex
cmd = 'cd ' + tmpdir + '; bibtex nobackup/main.aux'
print(cmd)
os.system(cmd)

shutil.copyfile(tmpdir + '/nobackup/main.bbl', tmpdir + '/main.bbl')

# htlatex
cmd = 'cd ' + tmpdir + '; htlatex main.tex "xhtml, charset=utf-8" " -cunihtf -utf8"'
print(cmd)
os.system(cmd)

# htlatex second run, necessary for bibliography?
cmd = 'cd ' + tmpdir + '; htlatex main.tex "xhtml, charset=utf-8" " -cunihtf -utf8"'
print(cmd)
os.system(cmd)

# change temporary PNGs to SVGs
figures.png2svgQuirk(tmpdir)

# CSS stuff
mycss.figs(tmpdir)
mycss.fonts(tmpdir)
mycss.body(tmpdir)
mycss.backtotop(tmpdir)

# HTML stuff
myhtml.mytitle(tmpdir, title, subtitle)
myhtml.myheadtitle(tmpdir, headtitle)
myhtml.viewport(tmpdir)
myhtml.toc(tmpdir)
myhtml.backtotop(tmpdir)
myhtml.bodyscrollx(tmpdir)

print('done')
