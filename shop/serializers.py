from rest_framework import serializers
from .models import Product, Order, Ticket

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'code', 'name', 'description', 'image']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'order', 'product_codes', 'status']