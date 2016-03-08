#!/usr/bin/env python

import webapp2
import urllib2
import re


class MainHandler(webapp2.RequestHandler):
	def get(self):
		url = "http://www.raptureready.com/"
		try:
			feed = urllib2.urlopen(url)
		except urllib2.URLError, e:
			handleError(e)
		pageContent = feed.read()

		# first find all the links
		matches = re.findall('< *[aA] *[hH][rR][eE][fF] *= *"(.+?(?=< *\/ *[aA]))', pageContent, re.DOTALL)
		#print(matches)

		# filter the link to the actual rapture index page
		linkToRaptureIndex = [elem for elem in matches if re.search('rapture *index', elem, re.IGNORECASE)]
		self.response.write(linkToRaptureIndex)

app = webapp2.WSGIApplication([
	('/', MainHandler)
], debug=True)
