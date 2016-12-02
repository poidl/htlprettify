#!/bin/python
# pylint: disable=C0103

"""HTML modifications"""

from bs4 import BeautifulSoup


def mytitle(path, newtitle):
    """Set an alternative HTML document title. Empty string is ignored
    (leaves old title in place)."""
    f = open(path + "/main.html")
    s = f.read()

    soup = BeautifulSoup(s, 'html.parser')

    title = soup.find_all('title')
    if newtitle:
        title[0].string.replace_with(newtitle)

    html = soup.prettify()
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

    html = soup.prettify()
    f = open(path + "/main.html", "w")
    f.write(html)


def toc(path):
    """Generate a table of content from tex files processed with htlatex"""
    f = open(path + "/main.html")
    s = f.read()

    soup = BeautifulSoup(s, 'html.parser')

    sectitlelist = soup.find_all('h3')
    ls = len(sectitlelist)
    ids = [[] for i in range(ls)]
    titles = ids.copy()

    for i in range(ls):
        l = sectitlelist[i]
        if l['class'] == ['sectionHead']:
            ids[i] = l.a['id']
            titles[i] = l.contents[4].strip()
            continue
        # the remaining one is for the bibliography, which is not numbered
        ids[i] = l.get('id')
        titles[i] = l.text.strip()

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
    # print(soup_ol.prettify())

    elem = soup.body.find_all("h3", {"class": "sectionHead"})[0]
    idx = soup.body.contents.index(elem)
    soup.body.contents.insert(idx, soup_ol.ol)
    html = soup.prettify()
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
        console.log('is scrolled')
        document.getElementById('back-to-top').style.display="inline-block"};
    </script>
    <div style="position: fixed; bottom: 25px; width=100%; max-width: 800px; margin:auto; text-align: right; left:0; right: 0;  padding-right: 1em;">
        <a href="#" id="back-to-top" class="back-to-top">Back to Top</a>
    </div>
"""

    soup_s = BeautifulSoup(s, 'html.parser')

    idx = soup.html.contents.index(soup.html.body)
    soup.contents.insert(idx, soup_s.script)
    soup.contents.insert(idx + 1, soup_s.div)
    html = soup.prettify()
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
    # html = soup.prettify()
    html = str(soup)
    f = open(path + "/main.html", "w")
    f.write(html)


def uglyhack(path, mystring):
    """Fix umlauts in \\emph{}"""
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

    html = soup.prettify()
    f = open(path + "/main.html", "w")
    f.write(html)
