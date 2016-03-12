#!/usr/bin/env python

import webapp2
import urllib2
import re


class MainHandler(webapp2.RequestHandler):
	def get(self):
		domain = "http://www.raptureready.com/"
		url = domain
		try:
			feed = urllib2.urlopen(url)
		except urllib2.URLError, e:
			handleError(e)
		pageContent = feed.read()

		# first find all the links
		matches = re.findall('< *a *href *= *"(.+?(?=< *\/ *a))', pageContent, re.DOTALL | re.IGNORECASE)
		#print(matches)

		# filter the link to the actual rapture index page
		linkToRaptureIndex = [elem for elem in matches if re.search('rapture *index', elem, re.IGNORECASE)]
		self.response.write(linkToRaptureIndex)

		# let's extract the path or absolute URL now
		# using this half-decent regex which should parse both the case
		# when this is a path and also a case where this is absolute.
		# if this fails, you can test this with the URLs here:
		#    https://mathiasbynens.be/demo/url-regex
		# also adding these examples:
		#    /blah_blah_(wikipedia)dd,dsd
		#    rap2.html">The Rapture Index'
		#    rap2.html
		#    ./miao.hmtl
		#    miao/miao/nanana/mamama/kdkd.html
		# using https://regex101.com/
		matches = re.findall('^((\.?\/?\w+)*\/?([\w\-\.]+[\w]+)([^\s\t\"]*)?(#[\w\-]+)?)', linkToRaptureIndex[0], re.IGNORECASE | re.MULTILINE)
		linkMatch = matches[0][0] + ""
		
		# now check if this is only a path then we need
		# to also add the domain and protocol.
		if not linkMatch.startswith('http://'):
			linkMatch = domain + linkMatch
		#self.response.write("<br>" + linkMatch)

		url = linkMatch
		try:
			feed = urllib2.urlopen(url)
		except urllib2.URLError, e:
			handleError(e)
		pageContent = feed.read()
		#self.response.write(pageContent)

		#
		# get all the index categories
		#
		matches = re.findall('<font face="Verdana" size="2">([^<]*)', pageContent, re.DOTALL | re.IGNORECASE)
		# eliminate empty items
		matches = [x for x in matches if x != ""]
		# stop at the "net change" item
		stopItem = next(x for x in matches if re.search('net *change', x, re.IGNORECASE))
		indexUpToWhichKeep = matches.index(stopItem)
		matches = matches[:indexUpToWhichKeep]

		self.response.write("<br>" + (', '.join(matches)))
		

app = webapp2.WSGIApplication([
	('/', MainHandler)
], debug=True)
