#
# -*- coding: UTF-8 -*-
from google.appengine.tools import bulkloader
from google.appengine.ext import db
#from fortune import Fortunes
from datetime import datetime

fmt="%Y-%m-%d %H:%M:%S"

class Fortunes(db.Model):
    fortune = db.StringProperty(multiline=True)
    author = db.StringProperty()
    categories = db.ListProperty(db.Category)
    rating = db.RatingProperty()
    lastshown = db.DateTimeProperty(auto_now_add=True)
    count = db.IntegerProperty()

def decatlist(input):
    ll=list()
    for l in input:
        ll.append('%s' % l.encode('utf8'))
    return "[u'%s']" % ("',u'".join(ll))


class FortuneExporter(bulkloader.Exporter):
    def __init__(self):
        bulkloader.Exporter.__init__(self,'Fortunes',[
            ('fortune',lambda x: x.encode('utf8'),None),
            ('author',lambda x: x.encode('utf8'),None),
            ('categories',decatlist,None),
            ('rating',lambda x: x==None and '0' or x ,None),
            ('lastshown',lambda x: x.strftime(fmt),None),
            ('count',lambda x: x==None and '0' or x ,None)
            ])

exporters = [FortuneExporter]

def catlist(input):
    input = input.decode('utf8')
    l = list()
    for c in eval(input):
        l.append(db.Category(c))
    return l

def loaddatetime(input):
    try:
        return datetime.fromtimestamp(float(input))
    except ValueError:
        return datetime.strptime(input,fmt)


class FortuneLoader(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self,'Fortunes',[
            ('fortune',lambda x: x.decode('utf8')[:500]),
            ('author',lambda x: x.decode('utf8')[:500]),
            ('categories',catlist),
            ('rating',db.Rating),
            ('lastshown',loaddatetime),
            ('count',int)
            ])

loaders = [FortuneLoader]

