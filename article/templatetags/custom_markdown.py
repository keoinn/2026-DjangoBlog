from django import template
from django.utils.safestring import mark_safe
import markdown

register = template.Library()


@register.filter(name='markdown_to_html')
def markdown_to_html(value):
    """
    將傳入的 Markdown 字串安全轉譯為 HTML
    """
    if not value:
        return ""
    
    html = markdown.markdown(
        value,
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            'markdown.extensions.fenced_code',
            'markdown.extensions.tables',
        ]
    )
    return mark_safe(html)
