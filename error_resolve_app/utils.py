from django.utils.html import mark_safe
import bleach
from markdown import markdown as markdown_func


def sanitize_markdown(value):
    return mark_safe(
            bleach.clean(
                markdown_func(value, extensions=['gfm'], tab_length=2),
                tags = [
                    'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em',
                    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                    'i', 'li', 'ol', 'p', 'pre', 'strong', 'ul',
                    'table', 'thead', 'tr', 'th', 'tbody', 'td',
                    'div', 'br', 'span',
                ],
            )
    )