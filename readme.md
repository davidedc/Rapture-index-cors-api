# What

A CORS-enabled API for [The Rapture index site](http://www.raptureready.com/) , self-described as follows: "the Rapture index is a Dow Jones Industrial Average of end time activity". The [related wikipedia page](https://en.wikipedia.org/wiki/Rapture_Ready) contains most interesting factoids about the index and the site.

Also of notable interest are [all the other Github projects based on the Rapture index](https://github.com/search?utf8=%E2%9C%93&q=rapture+index).

This API is used by my [Rapture Index Dashboard](https://github.com/davidedc/Rapture-index-dashboard).

# Why

There was this popular concept of "mashups" in the 90s: i.e. sets of scripts and web applications that could easily interoperate (directly within the browser) using datasets potentially coming from other domains, for example to visualise one dataset from a domain with a map application from another domain. This vision was particularly pushed by Yahoo, which also provided tools like Yahoo Pipes and YQL, where one could for example arbitrarily query websites as if they were databases, and could combine data coming from different domains with a dataflow-based visual language. (Yahoo Pipes and YQL are now in a general state of disrepair.)

Although some of these mechanisms still work, things have been made much more difficult lately by pervasive use of OAuth and API keys. OAuth and API keys complicate interoperability a lot, requiring complex flows and local servers / proxies (to keep the keys private) where otherwise a few lines of client-side javascript would have done the trick.

The reasons for this change are complex, it's got to do partly with security (very little), partly with the self-defense of API endpoints against attacks (lazy excuse), and partly because user-tracking always gives a business advantage. Case in example: [Google's URL shortener API](https://developers.google.com/url-shortener/v1/getting_started#OAuth2Authorizing) which for absolutely no reason requires OAuth/keys.

We'll eventually come back to that free-range-data-and-apps vision; in the meantime what we can do is to open services to serve data cross-domain, using CORS (which practically means adding a one-line header to the server response).


# How

This project runs on Google App Engine, which is a server solution that is practically free. This server parses the Rapture Index website (only if any requests are made, and at most once every hour) and serves the resulting JSON. Just do an AJAX GET on http://rapture-index-cors-api.appspot.com/ (or ```curl http://rapture-index-cors-api.appspot.com/ ``` from the command line) to get the JSON with the data. You can see a nice visualisation of the JSON clicking on [this link](http://jsonviewer.stack.hu/#http://rapture-index-cors-api.appspot.com/)

You can use my server (until it costs me) or just set up your own Google App Engine server.

# Disclaimer

There is no affiliation between this project and the Raptureready website. If you like the site, please consider donating to them [here](https://www.raptureready.com/rr-an-donation.php). 