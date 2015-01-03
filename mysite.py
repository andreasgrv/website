#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from flask import Flask, request, redirect, render_template, send_from_directory
from flask_bootstrap import Bootstrap

# create our application :)
app = Flask(__name__)
Bootstrap(app)

music_dir = 'static/music'
music_files = [f.split('.')[0] for f in os.listdir(music_dir)
               if f.endswith('.mp3')]

@app.route('/grv')
def homepage():
    return render_template('homepage.html')

@app.route('/grv/about')
def about():
    return render_template('about.html')

@app.route('/grv/read')
def reading():
    return render_template('read.html')

@app.route('/grv/listen')
def listen():
    return render_template('playlist.html', music_dir=music_dir,
                           music_files=enumerate(music_files))

@app.route('/grv/<fname>')
def download_file(fname):
    return send_from_directory(directory='files', filename=fname,
                               as_attachment=True)

if __name__ == '__main__':
    app.run(port=8080, host='inta.io', debug=False)
