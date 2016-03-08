#!/usr/bin/env python

import webapp2
import urllib2


class MainHandler(webapp2.RequestHandler):
	def get(self):
		url = "http://www.raptureready.com/"
		try:
			feed = urllib2.urlopen(url)
		except urllib2.URLError, e:
			handleError(e)
		self.response.write(feed.read())

app = webapp2.WSGIApplication([
	('/', MainHandler)
], debug=True)
