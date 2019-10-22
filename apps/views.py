from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
from org.models import Org


def index(r):
    return render(r, 'home.html', {})


def sitemap(r):
    return render(r, 'sitemap.xml', {'ls': Org.objects.all()})


@csrf_exempt
def search(r):
    q = r.GET.get('q', '')
    ls = Org.objects.filter(name__icontains=q).distinct()
    return render(r, 'search.html', {'q': q, 'ls': ls})


def autocomplete(r):
    q = r.GET.get('q', '').strip().lower()
    ls = ''
    if q:
        ls = Org.objects.filter(name__istartswith=q).order_by('name')[:10]
    return render_to_response('ac.html', {'ls': ls})
