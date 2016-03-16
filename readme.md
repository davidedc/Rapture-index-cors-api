# What

A CORS-enabled API for [The Rapture index site](http://www.raptureready.com/) , self-described as follows: "the Rapture index is a Dow Jones Industrial Average of end time activity". The [related wikipedia page](https://en.wikipedia.org/wiki/Rapture_Ready) contains most interesting factoids about the index and the site.

Also of notable interest are [all the other Github projects based on the Rapture index](https://github.com/search?utf8=%E2%9C%93&q=rapture+index).

This API is used by my [Rapture Index Dashboard](https://github.com/davidedc/Rapture-index-dashboard).

# Why

There was this popular concept of "mashups" in the 90s: i.e. sets of scripts and web applications that could easily interoperate (directly within the browser) using datasets potentially coming from other domains, for example to visualise one dataset with a map application. This vision was particularly pushed by Yahoo, which also provided tools like Yahoo Pipes and YQL, where one could for example arbitrarily query websites as if they were databases, and could combine flows of data coming from different domains.

Although some of these mechanisms still work, things have been made much more difficult lately by pervasive use of oauth and API keys. oauth and API keys complicate interoperability a lot, requiring complex flows and local servers of proxies (to keep the keys private) where otherwise a few lines of client-side javascript would have done the trick. Yahoo Pipes and YQL are in a general state of disrepair.

The reasons for this change are complex, it's got to do partly with security and the self-defense of API endpoints (both completely unwarranted most of the times, in my opinion).

We'll eventually go back to that vision - in the meantime what we can do is to open services to serve data cross-domain, using CORS (which practically means adding a one-line header to the server response).


# How

This project runs on Google App Engine, which is a server solution that is practically free. This server parses the Rapture Index website (only if any requests are made, and at most once every hour) and serves the resulting JSON. Just do a GET on http://rapture-index-cors-api.appspot.com/ (or ```curl http://rapture-index-cors-api.appspot.com/ ``` ) to get the JSON with the data. You can see a nice visualisation of the JSON clicking on [this link](http://jsonviewer.stack.hu/#http://rapture-index-cors-api.appspot.com/)

You can use my server (until it costs me) or just set up your own Google App Engine server.