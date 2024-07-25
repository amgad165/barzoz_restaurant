from rest_framework import serializers
from .models import *


class DeliveryFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryFee
        fields = ['fee']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'view_homepage', 'display_order']

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu_Item
        fields = ['id', 'name', 'description', 'price', 'category', 'image', 'display_order']

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['code', 'percent_off', 'duration', 'stripe_coupon_id']

class CustomerSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    phoneNumber = serializers.CharField(source='telefon')
    street = serializers.CharField(source='street_address')
    streetNumber = serializers.CharField(source='hausnummer')
    postalCode = serializers.CharField(source='plz_zip')
    city = serializers.CharField(source='bezirk')
    extraAddressInfo = serializers.CharField(source='um_hinweise', required=False)

    class Meta:
        model = User_details
        fields = ['name', 'phoneNumber', 'street', 'streetNumber', 'postalCode', 'city', 'extraAddressInfo']

    def get_name(self, obj):
        return f"{obj.vorname} {obj.nachname}"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['name'] = self.get_name(instance)
        return representation

class ProductSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='menu_item.id')
    name = serializers.CharField(source='menu_item.name')
    category = serializers.CharField(source='menu_item.category.name')
    count = serializers.IntegerField(source='quantity')
    price = serializers.DecimalField(source='menu_item.price', max_digits=10, decimal_places=2)
    remark = serializers.CharField(default="")

    class Meta:
        model = OrderItem
        fields = ['id', 'name', 'category', 'count', 'price', 'remark']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['name'] = instance.menu_item.name
        representation['category'] = instance.menu_item.category.name
        representation['price'] = instance.menu_item.price
        representation['remark'] = ""  # Placeholder for remarks if applicable
        return representation
    
class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(source='user_details')
    products = ProductSerializer(many=True, source='items')
    discounts = serializers.SerializerMethodField()
    orderDate = serializers.DateTimeField(source='ordered_date', format='%Y-%m-%dT%H:%M:%SZ')
    totalPrice = serializers.SerializerMethodField()
    deliveryFee = serializers.SerializerMethodField()
    orderType = serializers.CharField(default='delivery')
    courier = serializers.CharField(default='restaurant')
    platform = serializers.CharField(default='bazroz.com')

    deliveryCosts = serializers.DecimalField(max_digits=10, decimal_places=2, source='get_delivery_fee', read_only=True)  # Adjusted field
    isPaid = serializers.BooleanField(source='is_paid')
    paymentMethod = serializers.CharField(source='payment_type')
    remark = serializers.CharField(default='')
    version = serializers.CharField(default='1.1')
    clientKey = serializers.CharField(default='')
    serviceFee = serializers.FloatField(default=1.0)
    publicReference = serializers.CharField(default='')
    orderKey = serializers.CharField(source='id')

    class Meta:
        model = Order
        fields = ['id','platform','orderDate', 'orderType', 'courier', 'deliveryCosts', 'totalPrice', 
                  'isPaid', 'paymentMethod', 'customer', 'products', 'discounts', 'remark', 'version', 'clientKey',
                  'serviceFee', 'deliveryFee', 'publicReference', 'orderKey']

    def get_discounts(self, obj):
        if obj.coupon:
            return [{
                "name": "Discount",
                "count": 1,
                "price": obj.coupon.percent_off * -1
            }]
        return []

    def get_totalPrice(self, obj):
        return round(obj.get_total(), 2)

    def get_subtotalOrderPrice(self, obj):
        return round(obj.get_sub_total(), 2)

    def get_deliveryFee(self, obj):
        if obj.delivery_fee:
            return round(obj.delivery_fee.fee, 2)
        return None
    




class OrderStatusUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    status = serializers.CharField(max_length=50)
    key = serializers.CharField(max_length=100)
    changedDeliveryTimeString = serializers.DateTimeField()
    text = serializers.CharField(max_length=500)