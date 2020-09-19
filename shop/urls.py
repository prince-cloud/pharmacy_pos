from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import admin
from . import views



urlpatterns = [
    path('add-supply/', views.add_supply, name="add_supply"),
    path('add-product/', views.add_product, name="add_product"),
    path('add-purchase/', views.add_purchase, name="add_purchase"),
    path('add-expenses/', views.add_expense, name="add_expense"),
    path('history/', views.history, name="history"),
    path('history/<int:year>/', views.history, name="history"),
    path('history/<int:year>/<int:month>/', views.history, name="history"),
    path('history/<int:year>/<int:month>/<int:day>/', views.history, name="history"),
    path('drug/history/', views.drug_history, name="drug_history"),
    path('drug/history/<drug>/', views.drug_history, name="drug_history"),
    path('supply/history/', views.supply_history, name="supply_history"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('admin/', admin.site.urls, name='admin'),
    path('', views.items_list, name="items_list"),

]