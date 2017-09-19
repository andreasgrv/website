import os
import re
from collections import namedtuple
from markdown import markdown
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

CODE_RE = re.compile('<code class="(?P<lang>\w+)">(?P<code>.+?)</code>', re.DOTALL)
HTML_FORMATTER = HtmlFormatter(linenos=False)

page = namedtuple('Page', ('path', 'title', 'date', 'html'))

# need to cache this
def post_to_markdown(fname):
    try:
        with open(fname, 'r') as f:
            title = f.readline()
            date = f.readline()
            post = f.read()
    except Exception:
        return '404'
    i = 0
    segments = []
    md = markdown(post, ['markdown.extensions.extra'])
    for m in re.finditer(CODE_RE, md):
        segments.append(md[i:m.start()])
        hmd = highlight(m.group('code'),
                        get_lexer_by_name(m.group('lang')),
                        HTML_FORMATTER)
        segments.append(hmd)
        i = m.end()
    segments.append(md[i:])
    html = ''.join(segments)
    path = os.path.basename(fname).rsplit('.')[0]
    return page(path, title, date, html)
