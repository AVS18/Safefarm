from django.urls import path
from . import views
urlpatterns = [
    path('home',views.home,name="home"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('addProduct',views.addProduct,name="addProduct"),
    path('updateProduct',views.updateProduct,name="updateProduct"),
    path('acceptOrder/<int:id>',views.acceptOrder,name="acceptOrder"),
    path('rejectOrder/<int:id>',views.rejectOrder,name="rejectOrder"),
    path('orders',views.orders,name="order"),
    path('updateOrder/<int:id>',views.updateOrder,name="updateOrder")
]
