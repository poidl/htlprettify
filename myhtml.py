#!/bin/python
# pylint: disable=C0103

"""HTML modifications"""

import sys
from bs4 import BeautifulSoup


def mytitle(path, newtitle, newsubtitle):
    """Set alternative HTML document title and subtitle. Empty string is ignored
    (leaves old title in place)."""
    f = open(path + "/main.html")
    s = f.read()

    soup = BeautifulSoup(s, 'html.parser')

    title = soup.find_all('h2', {"class": "titleHead"})
    if newtitle:
        title[0].clear()
        title[0].append(newtitle)

        if newsubtitle:
            br = soup.new_tag('br')
            subt = soup.new_tag('h3')
            subt.append(newsubtitle)
            title[0].append(br)
            title[0].append(subt)

    html = str(soup)
    f = open(path + "/main.html", "w")
    f.write(html)


def myheadtitle(path, newtitle):
    """Set an alternative document title in <head> (title for browser tabs). Empty string is ignored
    (leaves old title in place)."""
    f = open(path + "/main.html")
    s = f.read()

    soup = BeautifulSoup(s, 'html.parser')

    title = soup.find_all('title')
    if newtitle:
        title[0].string.replace_with(newtitle)

    html = str(soup)
    f = open(path + "/main.html", "w")
    f.write(html)


def viewport(path):
    """Set the viewport."""
    f = open(path + "/main.html")
    s = f.read()

    soup = BeautifulSoup(s, 'html.parser')
    new_tag = soup.new_tag("meta")
    new_tag['name'] = "viewport"
    new_tag['content'] = "width=device-width, initial-scale=1"
    soup.head.append(new_tag)

    html = str(soup)
    f = open(path + "/main.html", "w")
    f.write(html)


def toc(path):
    """Generate a table of content from tex files processed with htlatex"""
    f = open(path + "/main.html")
    s = f.read()

    soup = BeautifulSoup(s, 'html.parser')

    sectitlelist = soup.find_all('h3', {"class": "sectionHead"})
    ls = len(sectitlelist)
    ids = [[] for i in range(ls)]
    titles = ids.copy()

    for i in range(ls):
        l = sectitlelist[i]
        ids[i] = l.a['id']
        titles[i] = l.contents[3].strip()

    # the remaining one should be the bibliography, which is not numbered
    bib = soup.find_all('h3', {"class": "likesectionHead"})
    l = bib[0]
    ids.append(l.get('id'))
    txt = l.text.strip()
    if txt != 'References':
        print('PROBLEM while scanning TOC entries. This should be the ' +
              'Bibliography section. ')

    titles.append(txt)

    # The html structure for an ordered list is:

    # <ol>
    #       <li><a href="HREF">NAME</a></li>
    # </ol>

    # HREF are fragment identifiers here (#)

    s1 = "<li><a href=\"#"
    s2 = "\">"
    s3 = "</a></li>"

    s1 = [s1] * ls
    s2 = [s2] * ls
    s3 = [s3] * ls

    z = list(zip(s1, ids, s2, titles, s3))
    labels = [''.join(str(x) for x in z[jj]) for jj in range(ls)]
    labels = ''.join(labels)

    ol = ''.join(["<ol>", labels, "</ol>"])

    soup_ol = BeautifulSoup(ol, 'html.parser')
    tag = soup_ol.new_tag("a")
    tag['id'] = "mycontents"
    soup_ol.li.insert_before(tag)
    # print(soup_ol.prettify())

    elem = soup.body.find_all("h3", {"class": "sectionHead"})[0]
    idx = soup.body.contents.index(elem)
    soup.body.contents.insert(idx, soup_ol.ol)
    html = str(soup)
    f = open(path + "/main.html", "w")
    f.write(html)


def backtotop(path):
    """Back-to-top button for long single-pages."""
    f = open(path + "/main.html")
    s = f.read()

    soup = BeautifulSoup(s, 'html.parser')

    s = """
    <script type="text/javascript">
        window.onscroll=function(){
            if (window.scrollY > 300 ) {
                document.getElementById('back-to-top').style.display="inline-block";
            } else {
                document.getElementById('back-to-top').style.display="none";
            }
        }
    </script>
    <div style="position: fixed; bottom: 25px; width=100%; max-width: 800px; margin:auto; text-align: right; left:0; right: 0;  padding-right: 1em;">
        <a href="#mycontents" id="back-to-top" class="back-to-top">Table of contents</a>
    </div>
"""

    soup_s = BeautifulSoup(s, 'html.parser')

    idx = soup.html.contents.index(soup.html.body)
    soup.contents.insert(idx, soup_s.script)
    soup.contents.insert(idx + 1, soup_s.div)
    html = str(soup)
    f = open(path + "/main.html", "w")
    f.write(html)


def remove_newlines_from_spans(path):
    """Umlauts in \\emph{} blocks cause spaces within a word. This does not
     solve the problem, but as a first step removes newlines in spans. The
     HTML file still needs to be modified manually."""
    f = open(path + "/main.html")
    s = f.read()

    soup = BeautifulSoup(s, 'html.parser')
    elem = soup.body.find_all("span", {"class": "cmssi-12"})
    [span.string.replace_with(span.get_text(strip=True)) for span in elem]
    # do not prettrify
    # html = str(soup)
    html = str(soup)
    f = open(path + "/main.html", "w")
    f.write(html)


def uglyhack(path, mystring):
    """Fix umlauts in \\emph{}. THIS IS NOT NECESSARY IF OUTPUT IS NOT PRETTYFIED (WITH EACH HTML/XML TAG ON ITS OWN LINE)"""
    f = open(path + "/main.html")
    s = f.read()
    soup = BeautifulSoup(s, 'html.parser')
    elem = soup.body.find_all("span", {"class": "cmssi-12"})
    # We search for the string with all spaces removed, to account for
    # (seemingly arbitrary) variations introduced by htlatex
    ms_alt = mystring.replace(' ', '')
    st = ""
    indices = []

    for i, e in enumerate(elem):
        st = st + e.text.strip().replace(' ', '')
        if st in ms_alt:
            indices.append(i)
            if st == ms_alt:
                elem[indices[0]].string.replace_with(mystring)
                for i in range(1, len(indices)):
                    elem[indices[i]].decompose()
                indices = []
                st = ""
            else:
                continue
        else:
            # start from scratch
            st = ""

    html = str(soup)
    f = open(path + "/main.html", "w")
    f.write(html)


def bodyscrollx(path):
    """Embed <body> in a <div> with overflow-x: scroll, to avoid viewport/page-zoom
    problems on mobile devices when a position: fixed element is present, which
    fixes relative to the viewport (e.g. Back-to-top button)."""
    f = open(path + "/main.html")
    s = f.read()
    soup = BeautifulSoup(s, 'html.parser')
    div = soup.new_tag("div", style="overflow-x: scroll;")
    soup.body.wrap(div)
    html = str(soup)
    f = open(path + "/main.html", "w")
    f.write(html)
