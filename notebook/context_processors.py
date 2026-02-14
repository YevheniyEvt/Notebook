from pygments.formatters import HtmlFormatter

_STYLE_NAME = 'default'
_PYGMENTS_CSS = HtmlFormatter(style=_STYLE_NAME).get_style_defs('.highlight')

def pygments_style(request):
    return {'pygments_css': _PYGMENTS_CSS}