#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#

from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.api import memcache
import os.path
from fortune import Fortunes
import random
import logging


class FortuneHandler(webapp.RequestHandler):

  def get(self):
    r = ""
    f = ""
    ff = ""
    pp = self.request.path
    p = os.path.basename(pp)
    while  p == '':
        pp = pp[:-1]
        p = os.path.basename(pp)

    #q = Fortunes.all()

    o = random.randint(0,9)
    l = 1
    if p != 'fortune':
        q = db.GqlQuery("SELECT * FROM Fortunes WHERE categories = :1 ORDER BY lastshown ASC LIMIT %i OFFSET %i " % (l,o), p)
    else:
        q = db.GqlQuery("SELECT *FROM Fortunes ORDER BY lastshown ASC LIMIT %i OFFSET %i" % (l,o) )

    #ffs = q.fetch(1000)
    #c = q.cursor()
    #ff += "<div>%r</div>" % c
    #q.with_cursor(c)

    #for ffs in Fortunes.all().filter('categories = ', os.path.basename(self.request.path)):
    #for ffs in q.with_cursor(c).fetch(1,1000):
    for ffs in q:
        ffs.count+=1
        ffs.lastshown=ffs.lastshown.now()
        ffs.put()
        #ff += "<div>%s</div>" % (memcache.get('123'))
        ff += """%s""" % (ffs.fortune.encode('utf8'))
    #ff = "%s" % (Fortunes.all().fetch(10))
    #q = db.GqlQuery("SELECT * From Fortunes")
    #for ffff in q:
    #    ff += "%s" % ffff.rating
    r += """<html>
    <head>
        <title>just fortunes</title>
        <!--
        <link rel="stylesheet" type="text/css" href="mystyles.css">
        -->
        <style type="text/css">
            body { font-family: helvetica; width: 600px; padding-left: 120px;}
            .fortune {}
        </style>
    </head>
    <body>
<div class="fortune">
    %s
</div>
    </body>
</html>""" % (ff)
    self.response.out.write(r)

class MainHandler(webapp.RequestHandler):

  def get(self):
    r="""
    """
    self.response.out.write(r)


class UserPrefs(db.Model):
    user = db.UserProperty()


class AdminHandler(webapp.RequestHandler):
  
  def get(self):
    user = users.get_current_user()
    r = ""
    if user:
        q = db.GqlQuery("SELECT * FROM UserPrefs WHERE user = :1", user)
        userprefs = q.get()

    self.response.headers.add_header('Content-type','text/plain')
    #for f in Fortunes.all():
    #for f in db.Query(Fortunes):
    #    r+="dleting: %s\n" % (f.fortune)
    #    #f.delete()
    self.response.out.write( r )




def main():
  application = webapp.WSGIApplication([
										('/', MainHandler),
										('/admin', AdminHandler),
										('/fortune',FortuneHandler),
										('/fortune/.*',FortuneHandler)
                                        ],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
