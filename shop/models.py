from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    code = models.CharField(max_length=50, unique=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    #comment = models.TextField(Product.code, blank=True)
    comment = models.TextField(blank=True, default="")

    def product_names(self):
        names = []
        for ticket in self.tickets.all():
            for code in ticket.product_codes:
                try:
                    product = Product.objects.get(code=code)
                    names.append(product.name)
                except Product.DoesNotExist:
                    names.append(f"(нет товара: {code})")
        return names

    STATUS_CHOICES = [
        ('PENDING', 'В ожидании'),
        ('IN_PROGRESS', 'В обработке'),
        ('DONE', 'Завершён'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order #{self.id} ({self.phone_number})"

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'В ожидании'),
        ('IN_PROGRESS', 'В обработке'),
        ('DONE', 'Завершён'),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tickets')
    product_codes = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    def __str__(self):
        return f"Ticket #{self.id} for Order #{self.order.id}"
