from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='products')
router.register(r'orders', views.OrderViewSet, basename='orders')
router.register(r'tickets', views.TicketViewSet, basename='tickets') 

urlpatterns = [
    path('', views.info,  name='info'),
    #path('info/', views.info, name='info'),
    path('catalogue/', views.cata, name='catalogue'),
    path('orders/', views.orders, name='orders'),
    path('api/', include(router.urls)),
    path('buy/', views.buy_product, name='buy_product'),
]