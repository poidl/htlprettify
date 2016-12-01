#!/bin/python
# pylint: disable=C0103

"""Generate a table of content from tex files processed with htlatex"""

from bs4 import BeautifulSoup

f = open("./main.html")
s = f.read()

soup = BeautifulSoup(s, 'html.parser')

sectitlelist = soup.find_all('h3')
ls = len(sectitlelist)
ids = [[] for i in range(ls)]
titles = ids.copy()
for i in range(ls):
    l = list(sectitlelist[i].children)
    if l[0].get('class') == ['titlemark']:
        ids[i] = l[2].get('id')
        titles[i] = l[3]
        continue
    # the remaining one is for the bibliography, which is not numbered
    ids[i] = l[0].get('id')
    titles[i] = l[1]

# The html structure for an ordered list is:

# <ol>
#       <li><a href="HREF">NAME</a></li>
# </ol>

# HREF are fragment identifiers here (#)

s1 = "<li><a href=\"#"
s2 = "\">"
s3 = "</a></li>"

s1 = [s1]*ls
s2 = [s2]*ls
s3 = [s3]*ls

z = list(zip(s1, ids, s2, titles, s3))
labels = [''.join(str(x) for x in z[jj]) for jj in range(ls)]
labels = ''.join(labels)

ol = ''.join(["<ol>", labels, "</ol>"])

soup = BeautifulSoup(ol, 'html.parser')
print(soup.prettify())


