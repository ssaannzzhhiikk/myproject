from django.shortcuts import render

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, permissions

from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib import messages

from .models import Product, Order, Ticket
from .serializers import ProductSerializer, OrderSerializer, TicketSerializer



# Create your views here.
def home(request):
    return render(request, "index.html")

def cata(request):
    products = Product.objects.all()
    return render(request, 'catalogue.html', {'products': products})

@login_required
def orders(request):
    user_orders = Order.objects.filter(user=request.user).prefetch_related('tickets')
    return render(request, 'orders.html', {'orders': user_orders})

def info(request):
    return render(request, 'info.html')


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Ticket.objects.all()
        return Ticket.objects.filter(order__user=self.request.user)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        ticket = self.get_object()
        new_status = request.data.get('status')
        if new_status not in dict(ticket.STATUS_CHOICES):
            return Response({'error': 'Invalid status'}, status=400)
        ticket.status = new_status
        ticket.save()
        return Response({'status': 'updated'})

def buy_product(request):
    if request.method == 'POST':
        product_code = request.POST.get('product_code')
        phone = request.POST.get('phone')

        if not product_code or not phone:
            messages.error(request, 'Заполните все поля.')
            return redirect('catalogue')

        # если пользователь авторизован — сохраняем связь
        user = request.user if request.user.is_authenticated else None

        # создаём заказ
        order = Order.objects.create(
            user=user,  # связь с пользователем
            phone_number=phone,
            status='PENDING',
            comment='Оформлен через сайт'
        )

        # создаём тикет и добавляем код товара
        ticket = Ticket.objects.create(order=order)
        ticket.product_codes.append(product_code)
        ticket.save()

        messages.success(request, 'Спасибо! Ваш заказ принят.')
        return redirect('catalogue')