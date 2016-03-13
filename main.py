#!/usr/bin/env python

import webapp2
import urllib2
import re
import json


class MainHandler(webapp2.RequestHandler):
	def get(self):
		
		# enable CORS from any domain
		self.response.headers.add_header("Access-Control-Allow-Origin", "*")
		self.response.headers['Content-Type'] = 'application/json'

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
		#self.response.write(linkToRaptureIndex)

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
		indexCategories = matches[:indexUpToWhichKeep]
		#self.response.write("<br>" + (', '.join(indexCategories)))

		#
		# get all the category values as strings (some of them contain +/- values as well)
		#
		matches = re.findall('[^ \d](\d+[-\+]?\d?)<[b\/s][rfut]', pageContent, re.DOTALL | re.IGNORECASE)
		categoryValues = matches
		#self.response.write("<br>" + categoryValues + " length: " + str(len(matches)))

		#
		# get the rapture index
		#
		raptureIndexValue = re.findall('rapture +index +(\d+)', pageContent, re.DOTALL | re.IGNORECASE)
		#self.response.write("<br>" + raptureIndexValue)

		#
		# get the net change
		#
		matches = re.findall('Net Change(&nbsp;)*[ \n\r\t]*(\+?-?\d+)', pageContent, re.DOTALL | re.IGNORECASE)
		netChange = matches[0][1]
		#self.response.write("<br>" + netChange)

		#
		# get the updated date
		#
		matches = re.findall('updated (.+?)(<\/font)', pageContent, re.DOTALL | re.IGNORECASE)
		updatedDate = matches[0][0]
		#self.response.write("<br>" + updatedDate)

		#
		# record high
		#
		matches = re.findall('record *high *(\d*)', pageContent, re.DOTALL | re.IGNORECASE)
		recordHigh = matches[0]
		#self.response.write("<br>" + recordHigh)
		
		#
		# record low
		#
		matches = re.findall('record *low *(\d*)', pageContent, re.DOTALL | re.IGNORECASE)
		recordLow = matches[0]
		#self.response.write("<br>" + recordLow)

		#
		# high date and low date
		#
		matches = re.findall('(([0-9])|([0-2][0-9])|([3][0-1]))\ (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\ (\d{4})', pageContent, re.DOTALL | re.IGNORECASE)
		highDate = matches[0][2] + " " + matches[0][4] + " " +  matches[0][5]
		lowDate = matches[1][2] + " " + matches[1][4] + " " +  matches[1][5]
		#self.response.write("<br>" + highDate)
		#self.response.write("<br>" + lowDate)
		
		#
		# notes headlines numbers
		#
		matches = re.findall('^(\d\d) [\w \/\-\\(\\)]*:?$', pageContent, re.IGNORECASE | re.MULTILINE)
		notesHeadlinesNumbers = matches
		#self.response.write("<br>" + notesHeadlinesNumbers)

		#
		# notes headlines
		#
		matches = re.findall('^\d\d ([\w \/\-\\(\\)]*):?$', pageContent, re.IGNORECASE | re.MULTILINE)
		notesHeadlines = matches
		#self.response.write("<br>" + notesHeadlines)
		
		#
		# notes bodies
		#
		matches = re.findall('[^>]<pre class="style1">(.+?(?=<\/pre))', pageContent, re.DOTALL | re.IGNORECASE | re.MULTILINE)
		notesBodiesText =  ('\n'.join(matches)) + "\n99"
		#self.response.write("<br>" + notesBodies)

		#
		# notes bodies
		#
		matches = re.findall('^    (.+?(?=\n\d))', notesBodiesText, re.DOTALL | re.IGNORECASE | re.MULTILINE)
		notesBodies = matches
		#self.response.write("<br>" + notesBodies)



		# now generate the JSON
		# you can debug the JSON here: http://jsonviewer.stack.hu/
		obj = {
			'linkToRaptureIndex': linkMatch, 
			'indexCategories': indexCategories,
			'categoryValues': categoryValues,
			'raptureIndexValue': raptureIndexValue,
			'netChange': netChange,
			'updatedDate': updatedDate,
			'recordHigh': recordHigh,
			'recordLow': recordLow,
			'highDate': highDate,
			'lowDate': lowDate,
			'notesHeadlinesNumbers': notesHeadlinesNumbers,
			'notesHeadlines': notesHeadlines,
			'notesBodies': notesBodies,
		}
		self.response.out.write(json.dumps(obj))		

app = webapp2.WSGIApplication([
	('/', MainHandler)
], debug=True)
