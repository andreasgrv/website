# website
My website

## Running the dev server

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python app/__init__.py
```

Then open <http://localhost:8000>. The server runs in debug mode, so it reloads
when Python files change. Template and CSS edits show up on a browser refresh.

Before the first run, check that:

- `APP_ROOT` in `create_app()` (`app/__init__.py`) points to this checkout.
  Templates, static files and posts are loaded from there, not from the current
  directory.
- `static/music/` exists, even if it's empty. The app lists that directory when
  it starts and fails if it's missing.

## Building the static site

```bash
python app/__init__.py --freeze
```

This writes a static copy of the site with Frozen-Flask (to `app/build/` by
default) and then starts the dev server as usual.
