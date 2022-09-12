from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name='catalog'

urlpatterns = [
    path(r'', views.Index,name='index'),
    path(r'commodity/', views.all_product, name='products'),
    path(r'brand/', views.all_brand, name='brand'),
    path(r'brand/<slug>/<int:id>/', views.all_product, name='brand_product'),
    path(r'commodity/<slug1>/<int:id>/', views.Commodity_Detail, name='commodity_detail'),
    path(r'classes/<int:id>/', views.all_product, name='classes'),
    path(r'like/<int:id>/', views.product_like, name='product_like'),
    path(r'unlike/<int:id>/', views.product_unlike, name='product_unlike'),
    path(r'comment/<int:id>/', views.product_comment, name='product_comment'),
    path(r'reply/<int:id>/<int:comment_id>', views.product_reply, name='product_reply'),
    path(r'like_comment/<int:id>/', views.comment_like, name='comment_like'),
    path(r'search/', views.product_search, name='product_search'),
    path(r'favourite/<int:id>', views.favourite_product, name='favourite'),
    path(r'contact/', views.contact, name='contact'),
      
] 
