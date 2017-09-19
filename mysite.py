#!/usr/bin/python
# -*- coding: utf-8 -*-
# based on flask examples

import os
import glob
import argparse
from datetime import datetime
from flask import Flask, render_template, send_from_directory
from flask_bootstrap import Bootstrap
from flask_frozen import Freezer
from blog_engine import post_to_markdown

# global options
DEBUG = True
# serve bootstrap locally
BOOTSTRAP_SERVE_LOCAL = True

BLOG_FOLDER = 'content'
POST_DIR = 'posts'

# calculate most recent modification to files
HTML_FILES = 'templates/*'
TIME_FORMAT = '%Y-%m-%d %H:%M'
MODIFIED = sorted(map(os.path.getmtime, glob.glob(HTML_FILES)))[-1]
LAST_EDITED = datetime.fromtimestamp(int(MODIFIED)).strftime(TIME_FORMAT)

# create our application :)
app = Flask(__name__)
# we want bootstrap!
Bootstrap(app)
# apply freezer to generate static pages
freezer = Freezer(app)

app.config.from_object(__name__)

# music_dir = 'files/music'
music_dir = 'static/music'
music_files = [f.split('.')[0] for f in os.listdir(music_dir)
               if f.endswith('.mp3')]

BLOG_POSTS = glob.glob('%s/%s/*.md' % (BLOG_FOLDER, POST_DIR))

POST_OBJECTS = sorted([post_to_markdown(p) for p in BLOG_POSTS],
                      key=lambda x: x.date,
                      reverse=True)

POST_HASH = dict([(p.path, p) for p in POST_OBJECTS])


@app.route('/')
def homepage():
    return render_template('homepage.html', posts=POST_OBJECTS, enumerate=enumerate)


@app.route('/posts/<name>/')
def post(name):
    """A page for each post

    :name: The name of the post
    :returns: The rendered page of this post

    """
    return render_template('post.html', post=POST_HASH[name])


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/read')
def reading():
    return render_template('read.html')


@app.route('/listen')
def listen():
    return render_template('playlist.html', music_dir=music_dir,
                           music_files=enumerate(music_files))


@app.route('/<fname>')
def download_file(fname):
    return send_from_directory(directory='files',
                               filename=fname,
                               as_attachment=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run server or freeze")
    parser.add_argument('--freeze', action='store_true',
                        dest='freeze', help='whether to create a static copy')
    args = parser.parse_args()
    if args.freeze:
        freezer.freeze()
    app.run(host='0.0.0.0', port=8000, debug=True)
