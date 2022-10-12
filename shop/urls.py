from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import admin
from . import views



urlpatterns = [
    path('', views.index, name="index"),
    path('add-supply/', views.add_supply, name="add_supply"),
    path('add-product/', views.add_product, name="add_product"),
    path('add-sale/', views.add_sale, name="add_sale"),
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
    path('items_list/', views.items_list, name="items_list"),
    path('history/page', views.history_page, name="history_page"),

    #new implementations
    path("store/", views.sale, name="store"),
    path("inventory/", views.inventory, name="inventory"),


]