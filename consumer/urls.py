from django.urls import path
from . import views
urlpatterns = [
    path('home',views.home,name="home"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('orderProduct',views.orderProduct,name="orderProduct"),
    path('catalogue',views.catalogue,name="catalogue"),
    path('orders',views.orders,name="orders")
]
