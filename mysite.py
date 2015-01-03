#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from flask import Flask, request, redirect, render_template, send_from_directory
from flask_bootstrap import Bootstrap

# create our application :)
app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def homepage():
	return render_template('homepage.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/read')
def reading():
	return render_template('read.html')

@app.route('/listen')
def listen():
	return render_template('listen.html')

@app.route('/contact')
def contact():
	return render_template('contact.html')

@app.route('/<fname>')
def download_file(fname):
	return send_from_directory(directory='files', filename=fname, as_attachment=True)

if __name__ == '__main__':
	app.run(port=8080, host='inta.io', debug=False)
