#!/usr/bin/python
# -*- coding: utf-8 -*-
# based on flask examples
# static blog example below:
# http://www.jamesharding.ca/posts/simple-static-markdown-blog-in-flask/

import os
import argparse
from flask import Flask, render_template, send_from_directory
from flask_bootstrap import Bootstrap
from flask_flatpages import FlatPages, pygments_style_defs
from flask_frozen import Freezer


# global options
DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = 'content'
POST_DIR = 'posts'

# create our application :)
app = Flask(__name__)
# we want bootstrap!
Bootstrap(app)
# use flatpages for blog
flatpages = FlatPages(app)
# apply freezer to generate static pages
freezer = Freezer(app)

app.config.from_object(__name__)

# music_dir = 'files/music'
music_dir = 'static/music'
music_files = [f.split('.')[0] for f in os.listdir(music_dir)
               if f.endswith('.mp3')]


@app.route('/')
def homepage():
    posts = [p for p in flatpages if p.path.startswith(POST_DIR)]
    posts.sort(key=lambda item: item['date'], reverse=False)
    return render_template('homepage.html', posts=posts, enumerate=enumerate)


@app.route('/posts/<name>/')
def post(name):
    """A page for each post

    :name: The name of the post
    :returns: The rendered page of this post

    """
    path = '%s/%s' % (POST_DIR, name)
    post = flatpages.get_or_404(path)
    return render_template('post.html', post=post)


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
    return send_from_directory(directory='files', filename=fname,
                               as_attachment=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run server or freeze")
    parser.add_argument('--freeze', action='store_true',
                        dest='freeze', help='whether to create a static copy')
    args = parser.parse_args()
    if args.freeze:
        freezer.freeze()
    app.run(host='46.101.23.192', port=8000, debug=True)
