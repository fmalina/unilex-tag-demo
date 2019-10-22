from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from django.conf import settings
from org.views import detail, after_joining, compose
from profile import profile
import views as main_views

slug = ''
urlpatterns = [
    path('', main_views.index),
    path('profile', profile, name='profile'),
    path('sitemap.xml', main_views.sitemap),
    path('sitemap<int:page>.xml', main_views.sitemap),
    path('search', main_views.search),
    path('autocomplete', main_views.autocomplete),

    path('<slug:slug>+<int:pk>', detail, name='org_detail'),
    path('edit/', include('org.urls')),

    re_path('^compose/(?P<recipient>[\w.@+-]+)/$', compose, name='compose_message'),
    path('after_joining', after_joining),

    path('product/', include('product.urls')),
    path('upload/', include('upload.urls')),
    path('messages/', include('django_messages.urls')),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('pay/', include('pay.urls')),
    path('account/', include('allauth.urls')),
    # uncomment if you don't use a reverse proxy
    re_path(r'^(.*)', serve, {'document_root': settings.STATIC_ROOT}),
]

admin.site.site_header = 'Fashion Sourcing'
admin.site.site_title = 'FS'
