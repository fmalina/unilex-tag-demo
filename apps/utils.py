from django.core.cache import cache
from django.conf import settings


def spoonfeed(qs, func, step=1000, i=0):
    while i < qs.order_by('-pk')[0].pk:
        for o in qs.filter(pk__gte=i).filter(pk__lt=i+step):
            func(o)
        i += step


def cached(key, func, args, expire=24*60*60):
    """ Usage: 
    expensive_call = lambda: [prices(r) for r in Region.objects.all()]
    prices = cached('prices', expensive_call, 24*60*60)
    """
    res = cache.get(key)
    if not res:
        res = func(*args)
        cache.set(key, res, expire)
    return res


def more_context(request):
    return {
        'domain': settings.DOMAIN,
        'site_url': settings.SITE_URL,
        'user': request.user
    }


def site_middleware(get_response):
    def middleware(request):
        try:
            request.page = int(request.path_info.split('.')[1])
        except (IndexError, ValueError):
            request.page = 1
        response = get_response(request)
        return response

    return middleware
