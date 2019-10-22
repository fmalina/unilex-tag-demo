from django.urls import path

from org import edit_org

urlpatterns = [
    path('new', edit_org.edit_new,
         name='org_new'),
    path('<int:pk>', edit_org.edit_contact,
         name='org_contact'),
]
