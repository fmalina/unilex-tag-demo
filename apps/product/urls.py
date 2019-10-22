from django.urls import path
from product.views import TaggingView, products, autocomplete

urlpatterns = [
    path('<slug:sector_slug>/add', TaggingView.as_view(template_name='product/product.html'), name="product_add"),
    path('list', products, name="products"),
    path('<int:pk>/edit', TaggingView.as_view(), name="product_edit"),
    path('<int:pk>', TaggingView.as_view(), name="product"),
    path('autocomplete', autocomplete, name="autocomplete"),
]
