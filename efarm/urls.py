from django.urls import path, include
from django.conf.urls import url
from . import views

app_name = 'efarm'
urlpatterns = [
    path('',views.index, name="index"),
    path('login',views.login, name="login"),
    path('signup',views.signup, name="signup"),
    path('logout',views.logout, name="logout"),
    path('welcome/farmer',views.welcomeFarmer, name="welcome_farmer"),
    path('welcome/customer',views.welcomeCustomer, name="welcome_customer"),
    path('farmer/addcrop',views.addCrop, name="addcrop"),
    url(r'^(?P<object_id>[0-9]+)/delete_crop/$', views.cropDelete, name='delete_crop'),
    url(r'^crop/(?P<pk>\d+)/edit/$', views.EditCrop.as_view(), name="edit-crop"),
    url(r'^crop/(?P<pk>\d+)/edit/$', views.EditCrop.as_view(), name="purchase-crop"),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.crop_detail, name='crop_detail'),
    url(r'^crop/$', views.crop_list, name='crop_list'),
    url(r'^crop/(?P<category_slug>[-\w]+)/$', views.crop_list, name='crop_list_by_category'),
    
    # path('charge/', views.charge, name='charge'),
    # path('payment', views.HomePageView.as_view(), name='home'),
]
