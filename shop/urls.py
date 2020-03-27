from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('add-supply/', views.add_supply, name="add_supply"),
    path('add-product/', views.add_product, name="add_product"),
    path('add-purchase/', views.add_purchase, name="add_purchase"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('', views.main, name="main"),
]