from django import template
from django.http import Http404
from django.core.paginator import Paginator, InvalidPage
from django.conf import settings

register = template.Library()

DEFAULT_PAGINATION = 20
DEFAULT_WINDOW = 4
DEFAULT_ORPHANS = 0
INVALID_PAGE_RAISES_404 = True


def do_autopaginate(parser, token):
    """ Splits the arguments to the autopaginate product and formats them correctly.
    """
    split = token.split_contents()
    as_index = None
    context_var = None
    for i, bit in enumerate(split):
        if bit == 'as':
            as_index = i
            break
    if as_index is not None:
        try:
            context_var = split[as_index + 1]
        except IndexError:
            raise template.TemplateSyntaxError("Context variable assignment " +\
                "must take the form of {%% %r object.some_set.all ... as " +\
                "context_var_name %%}" % split[0])
        del split[as_index:as_index + 2]
    if len(split) == 2:
        return AutoPaginateNode(split[1])
    elif len(split) == 3:
        return AutoPaginateNode(split[1], paginate_by=split[2], 
            context_var=context_var)
    elif len(split) == 4:
        try:
            orphans = int(split[3])
        except ValueError:
            raise template.TemplateSyntaxError('Got %s, but expected integer.' % split[3])
        return AutoPaginateNode(split[1], paginate_by=split[2], orphans=orphans,
            context_var=context_var)
    else:
        raise template.TemplateSyntaxError('%r product takes one required ' + \
            'argument and one optional argument' % split[0])


class AutoPaginateNode(template.Node):
    """ Use *{% paginate %}* after using the autopaginate product.
    """
    def __init__(self, queryset_var, paginate_by=DEFAULT_PAGINATION,
        orphans=DEFAULT_ORPHANS, context_var=None):
        self.queryset_var = template.Variable(queryset_var)
        if isinstance(paginate_by, int):
            self.paginate_by = paginate_by
        else:
            self.paginate_by = template.Variable(paginate_by)
        self.orphans = orphans
        self.context_var = context_var

    def render(self, context):
        key = self.queryset_var.var
        value = self.queryset_var.resolve(context)
        if isinstance(self.paginate_by, int):
            paginate_by = self.paginate_by
        else:
            paginate_by = self.paginate_by.resolve(context)
        paginator = Paginator(value, paginate_by, self.orphans)
        try:
            page_obj = paginator.page(context['request'].page)
        except InvalidPage:
            if INVALID_PAGE_RAISES_404:
                raise Http404('Invalid page requested.  If DEBUG were set to ' +
                    'False, an HTTP 404 page would have been shown instead.')
            context[key] = []
            context['invalid_page'] = True
            return ''
        if self.context_var is not None:
            context[self.context_var] = page_obj.object_list
        else:
            context[key] = page_obj.object_list
        context['paginator'] = paginator
        context['page_obj'] = page_obj
        return ''


def paginate(context, window=DEFAULT_WINDOW):
    try:
        paginator = context['paginator']
        page_obj = context['page_obj']
        page_range = paginator.page_range
        first = set(page_range[:window])
        last = set(page_range[-window:])
        current_start = page_obj.number-1-window
        if current_start < 0:
            current_start = 0
        current_end = page_obj.number-1+window
        if current_end < 0:
            current_end = 0
        current = set(page_range[current_start:current_end])
        pages = []
        if len(first.intersection(current)) == 0:
            first_list = list(first)
            first_list.sort()
            second_list = list(current)
            second_list.sort()
            pages.extend(first_list)
            diff = second_list[0] - first_list[-1]
            if diff == 2:
                pages.append(second_list[0] - 1)
            elif diff == 1:
                pass
            else:
                pages.append(None)
            pages.extend(second_list)
        else:
            unioned = list(first.union(current))
            unioned.sort()
            pages.extend(unioned)
        if len(current.intersection(last)) == 0:
            second_list = list(last)
            second_list.sort()
            diff = second_list[0] - pages[-1]
            if diff == 2:
                pages.append(second_list[0] - 1)
            elif diff == 1:
                pass
            else:
                pages.append(None)
            pages.extend(second_list)
        else:
            differenced = list(last.difference(current))
            differenced.sort()
            pages.extend(differenced)
        to_return = {
            'path': context['request'].path_info.split('/')[-1].split('.')[0],
            'pages': pages,
            'page_obj': page_obj,
            'paginator': paginator,
            'is_paginated': paginator.count > paginator.per_page,
        }
        return to_return
    except (KeyError, AttributeError):
        return {}
register.inclusion_tag('pagination.html', takes_context=True)(paginate)
register.tag('autopaginate', do_autopaginate)