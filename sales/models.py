from django.db import models,DatabaseError
from django.db.models.signals import pre_save, pre_delete
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from catalog.models import Product
from sites.models import Site
from account.models import Address


class Order(models.Model):
    """Order Model"""

    order_id = models.IntegerField(_('Order entity ID'))
    increment_id = models.CharField(_('Order increment ID'), max_length=255)
    site = models.ForeignKey(Site)

    state = models.CharField(_("Order state"),max_length=64)
    status = models.CharField(_("Order status"),max_length=64)

    coupon_code = models.CharField(_('Coupon code'),blank=True,null=True,max_length=254)
    shipping_description = models.CharField(_('Shipping description'),max_length=254)

    shipping_method = models.CharField(_('Shipping method'),max_length=254)

    shipping_address = models.ForeignKey(Address,related_name="shipping_address_id")
    billing_address = models.ForeignKey(Address,related_name ="billing_address_id")

    subtotal = models.DecimalField(_("Subtotal"),max_digits = 10,decimal_places=2)
    grand_total = models.DecimalField(_("Grand total"),max_digits = 10,decimal_places=2)
    base_currency_code = models.CharField(_('Base currency code'),max_length=254)
    currency_code = models.CharField(_('Order currency code'),blank=True,null=True,max_length=32)
    currency_rate =  models.DecimalField(_("Currency rate"),max_digits = 10,decimal_places=2)
    customer_email = models.EmailField(_('Customer email'))
    customer_firstname = models.CharField(_('Customer first name'),max_length=254)
    customer_lastname = models.CharField(_('Customer last name'),max_length=254)
    customer_middlename = models.CharField(_('Customer middle name'),blank=True,null=True,max_length=254)
    customer_prefix = models.CharField(_('Customer prefix'),blank=True,null=True,max_length=254)
    customer_suffix = models.CharField(_('Customer suffix'),blank=True,null=True,max_length=254)
    created_at = models.DateTimeField(_('Created At'),auto_now_add= True)
    updated_at = models.DateTimeField(_('Updated At'),auto_now_add= True)

    class Meta:
        unique_together = [("order_id","site"),("increment_id","site"),]


class OrderItem(models.Model):
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product)
    sku = models.CharField(_("SKU"),max_length=254)
    name = models.CharField(_("Product name"),max_length=254)
    free_shipping = models.BooleanField(_("Is free shipping"))
    qty_ordered = models.IntegerField(_("Qty Ordered"))
    qty_shipped = models.IntegerField(_("Qty Shipped"))
    qty_canceled = models.IntegerField(_("Qty Canceled"))
    qty_refunded = models.IntegerField(_("Qty Refunded"))
    price = models.DecimalField(_("Price"), max_digits= 10,decimal_places=2)
    original_price = models.DecimalField(_("Original price"), max_digits= 10,decimal_places=2)
    discount_amount = models.DecimalField(_("Discount amount"), max_digits= 10,decimal_places=2)


    class Meta:
        unique_together = [("order","product")]


class Shipment(models.Model):
    increment_id = models.CharField(_("Shipment increment ID"),max_length=254)
    order = models.ForeignKey(Order)
    shipping_address = models.ForeignKey(Address)
    created_at = models.DateTimeField(_('Created At'),auto_now_add= True)
    updated_at = models.DateTimeField(_('Updated At'),auto_now_add= True)


class ShipmentTrack(models.Model):
    parent = models.ForeignKey(Shipment)
    track_number = models.CharField(_("Track number"),max_length=254)
    title = models.CharField(_("Title"),max_length=254)
    carrier_code = models.CharField(_("Carrier code"),max_length=254)
    created_at = models.DateTimeField(_('Created At'),auto_now_add= True)
    updated_at = models.DateTimeField(_('Updated At'),auto_now_add= True)


class Payment(models.Model):
    order = models.ForeignKey(Order)
    increment_id = models.CharField(_("Shipment increment ID"),max_length=254)
    shipping_captured = models.DecimalField(_("Shipping Captured"),max_digits=10,decimal_places=2)
    amount_paid = models.DecimalField(_("Amount paid"),max_digits=10,decimal_places=2)
    amount_ordered = models.DecimalField(_("Amount ordered"),max_digits=10,decimal_places=2)
    last_trans_id = models.CharField(_("Last Trans Id"),max_length=254)
    method =  models.CharField(_("Payment method"),max_length=254)
    additional_information = models.TextField(_("Additional information"))


class Creditmemo(models.Model):

    order = models.ForeignKey(Order)
    subtotal = models.DecimalField(_("Subtotal"),max_digits = 10,decimal_places=2)
    grand_total = models.DecimalField(_("Grand total"),max_digits = 10,decimal_places=2)
    adjustment =  models.DecimalField(_("Adjustment"),max_digits = 10,decimal_places=2)
    created_at = models.DateTimeField(_('Created At'),auto_now_add= True)
    updated_at = models.DateTimeField(_('Updated At'),auto_now_add= True)



