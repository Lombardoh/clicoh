from django.contrib import admin
from stock_manager.models import Product, OrderDetail, Order

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
    pass

class OrderDetailInline(admin.TabularInline):
    model = OrderDetail

class OrderAdmin(admin.ModelAdmin):
    inlines=[OrderDetailInline]
    pass


admin.site.register(Product, ProductAdmin)

admin.site.register(Order, OrderAdmin)