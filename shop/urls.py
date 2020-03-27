from django.urls import path

from . import views

urlpatterns = [
    path('add-supply/', views.add_supply, name="add_supply"),
    path('add-product/', views.add_product, name="add_product"),
    path('add-purchase/', views.add_purchase, name="add_purchase"),
    path('', views.main, name="main"),
]