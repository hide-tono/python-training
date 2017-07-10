import re
from urllib.request import urlopen

from bs4 import BeautifulSoup

pages = set()
pagesAll = set()


def getLinks(pageUrl, depth):
    # print(' ' * depth, "searching:", pageUrl)
    global pages
    global pagesAll
    html = urlopen(pageUrl)
    bsObj = BeautifulSoup(html, "html.parser")
    try:
        print(' ' * depth, bsObj.h1.get_text())
    except AttributeError:
        pass
        # print("This page is missing something! No worries though!")

    local_pages = set()
    for link in bsObj.findAll("a", href=re.compile("^(/.*/|http://www.daisanbank.co.jp/.+)$")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                if link.attrs['href'] not in pagesAll:
                    # print(' ' * depth, 'new:', link.attrs['href'])
                    local_pages.add(link.attrs['href'])
                pagesAll.add(link.attrs['href'])

    for link in bsObj.findAll("a", href=re.compile("^(http://www.daisanbank.co.jp/.+)$")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                if link.attrs['href'] in pagesAll and link.attrs['href'] not in local_pages:
                    continue
                if ignore(link.attrs['href']):
                    continue
                # We have encountered a new page
                newPage = link.attrs['href']
                print(' ' * depth, "----------------\n", ' ' * depth, newPage)
                pages.add(newPage)
                getLinks(newPage, depth + 1)
    for link in bsObj.findAll("a", href=re.compile("^(/.*/)$")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                if link.attrs['href'] in pagesAll and link.attrs['href'] not in local_pages:
                    continue
                if ignore(link.attrs['href']):
                    continue
                # We have encountered a new page
                newPage = link.attrs['href']
                print(' ' * depth, "----------------\n", ' ' * depth, newPage)
                pages.add(newPage)
                getLinks('http://www.daisanbank.co.jp/' + newPage, depth + 1)


def ignore(url):
    if re.match(".*tenpo-.*", url):
        return True
    if re.match(".*kensaku.*", url):
        return True
    if re.match(".*/release/.*", url):
        return True
    if re.match('.*.pdf', url):
        return True
    return False


getLinks("http://www.daisanbank.co.jp/index.html", 0)
