from django.conf.urls import url
from django.urls import  path
from . import views

app_name = 'orders'

urlpatterns = [
    url(r'^create/$', views.order_create, name='order_create'),
    url(r'payment/$', views.HomePageView, name='payment'),
    path('created/', views.charge, name='created')
]