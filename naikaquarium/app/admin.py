from django.contrib import admin
from django.http import request
from .models import Customer, Product, Cart, OrderPlaced, Offer
from django.utils.html import format_html
from django.urls import reverse
from import_export.admin import ImportExportModelAdmin



# Register your models here.
admin.site.site_header = 'Naik Aquarium & Pet Shop'


@admin.register(Offer)
class CustomerAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['heading', 'text']


@admin.register(Customer)
class CustomerAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'phone_number',
                    'house_number', 'locality', 'landmark', 'city']


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'title', 'description',
                    'original_price', 'price', 'category', 'product_img']

    def customer_info(self, obj):
        link = reverse("admin:app_customer_change",
                       args=[obj.customer.pk])
        return format_html("<a href='{}'>{}</a>", link, obj.customer.name)

@admin.register(Cart)
class CartModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'user', 'customer_info', 'product_info', 'quantity', 'order_date', 'order_status']  # Add 'customer in the list to display full address in one line in admin panel.'

    def customer_info(self, obj):
        link = reverse("admin:app_customer_change",
                       args=[obj.customer.pk])
        return format_html("<a href='{}'>{}</a>", link, obj.customer.name)
    
    def product_info(self, obj):
        link = reverse("admin:app_product_change",
                       args=[obj.product.pk])
        return format_html("<a href='{}'>{}</a>", link, obj.product)