from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=False)
def link(name, url=''):
    if url and not url.startswith('/'):
        url='/'+url
    site = 'https://unilexicon.com'
    return site + url


@register.simple_tag(takes_context=True)
def tabs(context):
    get = lambda key: context.get(key, '')
    x = url = ''

    for tab in []:
        current = current_url = ''
        relevant_url = url
        if tab == get('org'):
            current = ' class="curr"'
            current_url = '#'
        x += '<li%s><a href="%s">%s</a></li>' % (
            current, current_url or link(tab, relevant_url), tab.title()
        )
    return mark_safe(x)
