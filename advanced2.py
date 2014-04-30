#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
Extra advanced features we will cover if we have time
like: multithreading requests, serializing (writing)
non-ascii html into a file via unicode/codecs.
"""

# Powerful web library we will be using to download html.
import urllib2

# HTML parsing library we will be using.
# Slow but easy to install & use for purposes of this workshop.
from BeautifulSoup import BeautifulSoup

# Our custom written multithreading framework.
# View the mthreading.py file for details.
from mthreading import Worker, ThreadPool

# Encoding aware file writer library.
import codecs

MIN_URL_LEN = 10

# Utility functions

def is_valid_url(url):
    """
    Note that this function fails for the scenario when the
    url is relative. We can write a seperate function
    to fix this.

    def fix_relative(url): which converts:
    "/news/blah.html" ==> "http://cnn.com/news/blah.html"
    """
    if not url or len(url) < MIN_URL_LEN:
        return False
    if url[:4] != 'http':
        return False

    # Perhaps you can brainstorm more on what checks
    # we can have. We can even try to filter out ad links.

    return True


def get_title(soup):
    """
    Extracts the <title> from an HTML page.
    """
    return soup.title.string


def get_links(soup):
    """
    """
    # Locate all <a> tags on the html page.
    link_tags = soup.findAll('a')

    # Extract out only the 'href' portion of the link <a> tag.
    links = [tag.get('href') for tag in link_tags]

    # Ensure the links are valid according to our standards
    links = [link for link in links if is_valid_url(link)]
    return links


url_one = u'http://sports.yahoo.com/blogs/nhl-puck-daddy/marc-andre-fleury--playoff-disaster--is-holding-penguins-back-from-stanley-cup--trending-topics-135956057.html'

url_two = u'http://dailynews.yahoo.co.jp/fc/domestic/ianfu/?id=6114793'


# Example on how to apply multithreading to send out requests
# -----------------------------------------------------------

class MRequest(object):
    """
    Wrapper for sending out a multithreaded request
    """
    def __init__(self, url):
        self.url = url

    def send(self):
        request = urllib2.Request(self.url)
        self.resp = urllib2.urlopen(request)

# We allocate 10 threads to download from 2 urls.
numb_threads = 10
pool = ThreadPool(numb_threads)
urls = [url_one, url_two]
reqs = []

for url in urls:
    reqs.append(MRequest(url))

# Call send() together concurrently
for req in reqs:
    pool.add_task(req.send)

pool.wait_completion()

# reqs should now be populated with filled responses

print 'length of multithreaded html', len(reqs[0].resp.read()), len(reqs[1].resp.read())


# Example on how to write data into a file.
# -----------------------------------------

"""
# Bad example. Not unicode aware and will result in a
# decoding error.
f = open('japan.txt', 'w')
f.write(html_two)
f.close()
"""

"""
# Good example on how to store data from the web.
f = codecs.open('japan.txt', 'w', 'utf8')
f.write(html_two)
f.close()
"""

"""
f = codecs.open('japan.txt', 'r', 'utf8')
stored_html = f.read()
print stored_html
f.close()
"""
