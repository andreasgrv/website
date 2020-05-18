# based on flask examples
# static blog example below:
# http://www.jamesharding.ca/posts/simple-static-markdown-blog-in-flask/

import os
import argparse
import requests
import markdown
from datetime import datetime
from glob import glob
from flask import Flask, render_template, url_for, request
from flask import send_from_directory, render_template_string
from flask_flatpages import FlatPages
from flask_flatpages.utils import pygmented_markdown
from flask_frozen import Freezer
from flask_migrate import Migrate

from methinks.db import db
from app.methinks import methinks_routes


TIME_FORMAT = '%A, %d %B %Y at %H:%M'
DB_URI = 'postgresql://%s:%s@localhost/%s' % (os.environ['METHINKS_DB_USER'],
                                              os.environ['METHINKS_DB_PASSWD'],
                                              os.environ['METHINKS_DB_NAME'])


def create_app():
    APP_ROOT = '/home/grv/website'
    TEMPLATE_FOLDER = '%s/templates' % APP_ROOT
    STATIC_FOLDER = '%s/static' % APP_ROOT

    app = Flask(__name__,
                template_folder=TEMPLATE_FOLDER,
                static_folder=STATIC_FOLDER)

    app.config['APP_ROOT'] = APP_ROOT
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['FLATPAGES_EXTENSION'] = '.md'
    app.config['FLATPAGES_ROOT'] = '%s/content/posts' % APP_ROOT
    app.config['FLATPAGES_MARKDOWN_EXTENSIONS'] = ['markdown.extensions.fenced_code',
                                                   'markdown.extensions.codehilite',
                                                   'markdown.extensions.footnotes',
                                                   'markdown.extensions.tables']
    # calculate most recent modification to files
    HTML_FILES = '%s/templates/*' % APP_ROOT
    MODIFIED = sorted(map(os.path.getmtime, glob(HTML_FILES)))[-1]
    app.config['LAST_EDITED'] = datetime.fromtimestamp(int(MODIFIED)).strftime(TIME_FORMAT)

    app.register_blueprint(methinks_routes, url_prefix='/methinks')

    db.init_app(app)
    migrate = Migrate(app, db)
    return app


# create our application :)
app = create_app()
# use flatpages for blog
flatpages = FlatPages(app)
# apply freezer to generate static pages
freezer = Freezer(app)

# Below stolen from
# https://gist.github.com/chrisma/dad9e71de343b4cd6e5c
@app.template_filter()
def hex_to_rgb(hexcode, format_string='{r},{g},{b}'):
    """Returns the RGB value of a hexadecimal color"""
    hexcode = hexcode.replace('#', '')
    out = {	'r':int(hexcode[0:2], 16),
            'g':int(hexcode[2:4], 16),
            'b':int(hexcode[4:6], 16)}
    return format_string.format(**out)

def my_renderer(text):
    prerendered_body = render_template_string(text)
    return pygmented_markdown(prerendered_body, flatpages)


app.config['FLATPAGES_HTML_RENDERER'] = my_renderer
app.register_blueprint(methinks_routes, url_prefix='/methinks')


# music_dir = 'files/music'
music_dir = '%s/static/music' % app.config['APP_ROOT']
music_files = [f.split('.')[0] for f in os.listdir(music_dir)
               if f.endswith('.mp3')]


@app.route('/')
def homepage():
    return render_template('about.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/log')
def log():
    posts = [p for p in flatpages]
    posts.sort(key=lambda item: datetime.strptime(item['date'], TIME_FORMAT), reverse=True)
    return render_template('log.html', posts=posts, enumerate=enumerate)


@app.route('/posts/<name>')
def post(name):
    """A page for each post

    :name: The name of the post
    :returns: The rendered page of this post

    """
    print(name)
    post = flatpages.get_or_404(name)
    return render_template('post.html', post=post)


@app.route('/diary/<date>')
def diary(date):
    """A page for diary entries

    :date: The date of the entry
    :returns: The rendered page of this post

    """
    url = url_for('methinks_routes.get_entry', date=date)
    methinks_endpoint = 'https://grv.overfit.xyz%s?token=%s' % (url, request.args.get('token', ''))
    r = requests.get(methinks_endpoint).json()
    entry = dict()
    if r['status']:
        data = r['data']
        entry['html'] = markdown.markdown(data['text'])
        entry['date'] = data['date']
        entry['last_edited'] = data['last_edited']
    return render_template('diary.html', entry=entry)


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
