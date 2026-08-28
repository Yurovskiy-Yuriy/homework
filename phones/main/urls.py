from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('phone/<int:phone_id>/', views.phone_detail, name='phone_detail'),
]