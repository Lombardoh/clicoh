from importlib.metadata import requires
from itertools import product
from rest_framework import serializers
from .models import Product, Order, OrderDetail
import requests, json

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderDetailerializer(serializers.ModelSerializer):
    price = serializers.FloatField(source='product.price')
    name = serializers.CharField(source='product.name')
    class Meta:
        model = OrderDetail
        fields = ['name','cuantity', 'price']

#order update

class OrderSerializer(serializers.ModelSerializer):
    order_details = OrderDetailerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField('get_total')
    total_usd = serializers.SerializerMethodField('get_total_usd')
    
    class Meta:
        model = Order
        fields = '__all__'
    
    def get_total(self, obj):
        total = 0
        for detail in obj.order_details.all():
            total = total + int(detail.cuantity) * float(detail.product.price)
        return total
    
    def get_total_usd(self, obj):
        response = requests.get('https://www.dolarsi.com/api/api.php?type=valoresprincipales')
        response_json = json.loads(response.text)
        precio_dolar = response_json[1]['casa']['compra']
        precio_dolar = float(precio_dolar.replace(',','.'))

        total = 0
        for detail in obj.order_details.all():
            total = total + int(detail.cuantity) * float(detail.product.price)
        total_usd = total / precio_dolar
        return "{:.2f}".format(total_usd)


#order creation

class OrderDetailCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ['cuantity', 'product']

class OrderCreateSerializer(serializers.ModelSerializer):
    order_details = OrderDetailCreateSerializer(many=False, read_only=True)
    class Meta:
        model = Order
        fields = '__all__'


