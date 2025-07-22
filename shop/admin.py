from django.contrib import admin
from .models import Order, Ticket, Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone_number', 'status', 'created_at', 'product_codes', 'product_names')

    def product_codes(self, obj):
        codes = []
        for ticket in obj.tickets.all():
            codes.extend(ticket.product_codes or [])
        return ", ".join(codes)
    product_codes.short_description = 'Код товара'

    def product_names(self, obj):
        codes = []
        for ticket in obj.tickets.all():
            codes.extend(ticket.product_codes or [])
        products = Product.objects.filter(code__in=codes)
        return ", ".join(p.name for p in products)
    product_names.short_description = 'Названия товара'

admin.site.register(Order, OrderAdmin)
admin.site.register(Ticket)
