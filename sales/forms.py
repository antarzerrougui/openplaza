from django.forms import ModelForm

from .models import Order,Payment,Shipment


class OrderModelForm(ModelForm):
    class meta:
        model = Order


class PaymentModelForm(ModelForm):
    class meta:
        model = Payment


class ShipmentModelForm(ModelForm):
    class meta:
        model = Shipment