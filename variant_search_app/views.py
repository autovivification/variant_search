#!/usr/bin/env python

from flask import render_template
from variant_search_app import app

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')
