from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('track/', views.track_shipment, name='track_shipment'),
]