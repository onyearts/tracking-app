from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('track/', views.track_shipment, name='track_shipment'),
    path('admin/generate-tracking/', views.generate_tracking_number_view, name='generate_tracking'),
    path('about/', views.about_page, name='about'),
    path('blog/', views.blog_page, name='blog'),
]