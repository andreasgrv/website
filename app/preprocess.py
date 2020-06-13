import re


MATHJAX = re.compile(r'(?P<all>\$\$(?P<math>.*?)\$\$)', flags=re.DOTALL)
ESCAPE_CHARS = '\\`*_{}[]()#+-.!'


def escape_math(match):
    s = match.group('all')

    for c in ESCAPE_CHARS:
        repl = '\\%s' % c
        s = s.replace(c, repl)

    return s


def escape_jax_for_markdown(text):
    return re.sub(MATHJAX, escape_math, text)
