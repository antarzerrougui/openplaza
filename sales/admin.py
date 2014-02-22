from django.contrib import admin
from .models import Order,OrderItem,Payment,Shipment
from .forms import OrderModelForm



class OrderItemInline(admin.StackedInline):
    model = OrderItem
    can_delete = False

class PaymentItemInline(admin.StackedInline):
    model = Payment
    can_delete = False
    max_num = 1

class ShipmentInline(admin.StackedInline):
    model = Shipment
    can_delete = False
    max_num = 1

class OrderAdmin(admin.ModelAdmin):
    search_fields = ('increment_id','customer_firstname')
    form = OrderModelForm

    inlines = (OrderItemInline,PaymentItemInline,ShipmentInline,)

admin.site.register(Order, OrderAdmin)
