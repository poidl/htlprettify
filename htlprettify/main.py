#!/bin/python
# pylint: disable=C0103

"""Post-process htlatex output"""

import configparser
import shutil
import os
import subprocess

import myutils
import figures
import mycss
import myhtml
# import htlprettify.myutils as myutils
# import htlprettify.figures as figures
# import htlprettify.mycss as mycss
# import htlprettify.myhtml as myhtml

config = configparser.ConfigParser()
config.read('./config')
conf = config['htlprettify']

path = conf['path']
figurepath = conf['figurepath']
installpath = conf['installpath']
installimgpath = conf['installimgpath']
tmpdir = conf['tmpdir']
title = conf['title']
subtitle = conf['subtitle']
headtitle = conf['headtitle']


def main():
    """Main function"""
    # Config arg sanity check
    myutils.pathsanitycheck(path, figurepath, installpath, installimgpath)
# Create build directory and copy latex source files
    if os.path.isdir(tmpdir):
        shutil.rmtree(tmpdir)
    os.mkdir(tmpdir)
    os.mkdir(tmpdir + '/nobackup')
    cp = myutils.Copier(path, tmpdir)
    cp.copy('main.tex')
    cp.copy('main.bib')
    cp.copy('model2-names.bst')
    # cp.copytree('figures')

    # Assumes use of pdflatex, or more generally, that figures included in the
    # latex source are PDFs. Furthermore assumes that for each PDF, an SVG of
    # the same name is present (SVG is best for HTML?). Substitute them
    # temporarily by PNGs, to avoid errors with latex and htlatex.

    # figures.pdf2pngQuirk(tmpdir)
    figures.adjustFigPath(tmpdir, figurepath)

    # Latex first run
    cmd = 'cd ' + tmpdir + '; pdflatex -synctex=1 -output-directory=nobackup' \
        + ' -halt-on-error -file-line-error main.tex|grep -n1 -i error'
    print(cmd)
    out = subprocess.getoutput(cmd)
    if out:
        raise Exception('********* Latex error *************\n' + out)

    # Bibtex
    cmd = 'cd ' + tmpdir + '; bibtex nobackup/main.aux'
    print(cmd)
    os.system(cmd)

    shutil.copyfile(tmpdir + '/nobackup/main.bbl', tmpdir + '/main.bbl')

    # htlatex
    cmd = 'cd ' + tmpdir + \
        '; htlatex main.tex "xhtml, charset=utf-8" " -cunihtf -utf8" |grep -n1 -i error'
    print(cmd)
    out = subprocess.getoutput(cmd)
    if out:
        raise Exception(
            '********* htlatex error (1st run) *************\n' + out)

    # htlatex second run, necessary for bibliography?
    print(cmd)
    out = subprocess.getoutput(cmd)
    if out:
        raise Exception(
            '********* htlatex error (2nd run) *************\n' + out)

    # Delete/create html install directory
    p = installpath
    if os.path.isdir(p):
        shutil.rmtree(p)
    os.mkdir(p)

    # Delete/create figure install directory only if it's not identical to the
    # latex source figure path. TODO: danger: may loose all figures.
    # Backup?
    installimgpath_abs = installpath + '/' + installimgpath
    p1 = os.path.abspath(figurepath)
    p2 = os.path.abspath(installimgpath_abs)
    if p1 != p2:
        p = p2
        if os.path.isdir(p):
            shutil.rmtree(p)
        os.mkdir(p)
        # move SVGs to imgrelpath
        figures.move(figurepath, installimgpath_abs)

    # substitute dummy PNGs with SVGs in html file ...
    figures.png2svgSubstitution(tmpdir, installimgpath_abs)
    # ... and temporarily change the html figure path to the absolute path, so
    # one can experiment with the css and html modifications below.
    figures.changeHtmlFigpath(tmpdir, installimgpath_abs)

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

    # final html figure path
    figures.changeHtmlFigpath(tmpdir, installimgpath)
    # copy to install dir
    cp = myutils.Copier(tmpdir, installpath)
    cp.copy('main.html')
    cp.copy('main.css')

    print('done')

if __name__ == '__main__':
    main()
