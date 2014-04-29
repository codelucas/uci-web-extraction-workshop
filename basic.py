# -*- coding: utf-8 -*-
import urllib2
from BeautifulSoup import BeautifulSoup


# Download the HTML
request = urllib2.Request('http://www.uci.edu')
response = urllib2.urlopen(request)

print '\r\n\r\n'

# Verify that everything went ok.
# Error codes: 200 == good, 404, 500 == bad
print 'The error code is:', response.code
print '\r\n\r\n'
html = response.read()

# Parse the HTML into a dom object via our BS library.
dom = BeautifulSoup(html)

# Extract out the <div> tag containing our news.
news_tag = dom.find('div', {'id': 'news'})

# See what the extracted HTML looks like.
print 'The extracted news div HTML looks like:'
print '===================================='
print news_tag
print '\r\n\r\n'

# Further extract out a list of the actual news titles.
news_li_tags = news_tag.findAll('li')
titles = [tag.text for tag in news_li_tags]
links = [tag.a['href'] for tag in news_li_tags]

print 'The top news titles on www.uci.edu are currently:'
print '===================================='
for title in titles:
    print title

print 'The top news links on www.uci.edu are currently:'
print '===================================='
for link in links:
    print link

print '\r\n\r\n'
