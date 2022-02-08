from stock_manager.models import Product, Order, OrderDetail
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import redirect
from rest_framework import serializers
from django.http import HttpResponse
from .serializers import ProductSerializer, OrderSerializer, OrderCreateSerializer

class produt_view_set(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class order_view_set(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=False, methods=['PUT'])
    def update(self, request, pk=None):
        order = Order.objects.get(pk = pk)
        products_data = request.data['order_details']
        products_dic =  {}

        for product_data in products_data:
            products_dic[product_data['product']] = product_data['cuantity']

        for order_detail in order.order_details.all():
            product = Product.objects.get(pk = order_detail.product.pk)
            product.stock = product.stock + order_detail.cuantity - products_dic[order_detail.product.pk]
            order_detail.cuantity = products_dic[order_detail.product.pk]
            product.save()
            if order_detail.cuantity == 0:
                OrderDetail.objects.get(order_detail.pk).delete()
            else:
                order_detail.save()
        
        print(products_dic)
        return redirect('/api/orders/')

class order_detail_view_set(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderCreateSerializer
    renderer_classes=[TemplateHTMLRenderer]
    template_name = 'order_creation.html'
    style = {'template_pack': 'rest_framework/vertical/'}

    @action(detail=True, methods=['GET'])
    def custom(self, request):
        serializer = OrderCreateSerializer()
        return Response({'serializer': serializer, 'style': self.style})

    @action(detail=False, methods=['POST'])
    def create(self, request, *args, **kwargs):
        #get products data and check for duplicates
        products_data = request.POST.getlist('order_details.product')
        products_set = set(products_data)
        contains_duplicates = len(products_data) != len(products_set)
        if contains_duplicates:
            return HttpResponse({'Duplicated products'})

        cuantity_data = request.POST.getlist('order_details.cuantity')

        #validate that cuantities are 1 or more
        for cuantity in cuantity_data:
            if int(cuantity) < 1:
                return HttpResponse({'Cuantity cannot be lower than 1'})

        #check stock before creating order
        for idx, val in enumerate(products_data):
            product = Product.objects.get(pk = products_data[idx])
            if product.stock < int(cuantity_data[idx]):
                return HttpResponse({'not enough stock'})

        #this new order will be used to attach products and cuantities
        order =  Order.objects.create()

        #once validations are done details can be attached to the order and cuantity can be substracted from stock
        for idx, val in enumerate(products_data):
            product = Product.objects.get(pk = products_data[idx])
            product.stock = product.stock - int(cuantity_data[idx])
            product.save()
            OrderDetail.objects.create(order = order, cuantity = cuantity_data[idx], product = product)
        
        return redirect('/api/orders/create')
