from django.urls import path
from . import views

app_name = 'wallet'

urlpatterns = [
    path('', views.address_list, name='address_list'),
    path('add/', views.add_address, name='add_address'),
    path('remove/<int:pk>/', views.remove_address, name='remove_address'),
    path('sync/', views.sync_address, name='sync_all_addresses'),
    path('sync/<int:pk>/', views.sync_address, name='sync_address'),
    path('address/<int:pk>/', views.address_detail, name='address_detail'),
] 