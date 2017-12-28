#!/usr/bin/env python

from variant_search_db.dbhandler import DbHandler
import json
from datetime import datetime
from flask import Flask

app = Flask(__name__)
dbh = DbHandler()

mimetype = 'application/json'
valid_search_methods = ['startswith', 'contains']

class JsonDateTimeEncoder(json.JSONEncoder):
    """
    Use a custom encoder for processing and encoding DateTime 
    prior to dumping JSON
    """
    def default(self, o):
        try:
            return super(JsonDateTimeEncoder, o).default(o)
        except TypeError:
            return str(o)

import variant_search_app.api
