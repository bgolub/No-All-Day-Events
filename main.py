#!/usr/bin/env python

from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

class MainHandler(webapp.RequestHandler):
    def get(self):
        try:
            response = urlfetch.fetch(self.request.get('url'))
        except (urlfetch.DownloadError, urlfetch.InvalidURLError):
            return self.error(404)
        buffer = []
        skip = False
        output = []
        for line in response.content.split('\r\n'):
            if line.startswith('BEGIN') and len(buffer) and not skip:
                output.extend(buffer)
                buffer = []
            buffer.append(line)
            if line.startswith('END') and len(buffer):
                if not skip:
                    output.extend(buffer)
                buffer = []
                skip = False
            if line.startswith('DTSTART') and 'DATE' in line:
                skip = True
        output.extend(buffer)
        self.response.headers['Content-Type'] = response.headers['Content-Type']
        self.response.out.write('\r\n'.join(output))


def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
