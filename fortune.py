#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from google.appengine.ext import db
from datetime import datetime

class Fortunes(db.Model):
    fortune = db.StringProperty(multiline=True)
    author = db.StringProperty()
    categories = db.ListProperty(db.Category)
    rating = db.RatingProperty()
    lastshown = db.DateTimeProperty(auto_now_add=True)
    count = db.IntegerProperty()
