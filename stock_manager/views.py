from stock_manager.models import Product, Order, OrderDetail
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import redirect
from django.http import HttpResponse
from .serializers import ProductSerializer, OrderSerializer, OrderCreateSerializer
from rest_framework.permissions import IsAuthenticated

class produt_view_set(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class order_view_set(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=True, methods=['DELETE'])
    def destroy(self, request, pk=None):
        order = Order.objects.get(pk = pk)
        for order_detail in order.order_details.all():
            product = Product.objects.get(pk = order_detail.product.pk)
            product.stock = product.stock + order_detail.cuantity
            product.save()
        order.delete()
        return HttpResponse({f'Orden {order.id}borrada'})

    @action(detail=True, methods=['PUT'])
    def update(self, request, pk=None):

        order = Order.objects.get(pk = pk)
        products_data = request.data['order_details']

        products_dict = {}
        products_list = []
        for product_data in products_data:
            products_list.append(product_data['id'])
            products_dict[product_data['id']] = product_data
        
        products_set = set(products_list)
        
        contains_duplicates = len(products_list) != len(products_set)
        if contains_duplicates:
            return HttpResponse({"Productos duplicados"})

        for product_id in products_list:
            product = Product.objects.get(id = str(product_id))
            order_details_obj = []
            try:
                order_details_obj = order.order_details.all().get(product = product)
            except: 
                order_details_obj = OrderDetail.objects.create(order = order, product = product, cuantity = products_dict[product_id]['cuantity'])
                
            product.stock = product.stock + int(order_details_obj.cuantity) - int(products_dict[product_id]['cuantity'])
            order_details_obj.cuantity = int(products_dict[product_id]['cuantity'])
            order_details_obj.save()
            if product.stock < 0:
                    return HttpResponse({f"No hay suficiente stock del producto {product.name}"})
            product.save()
            if int(products_dict[product_id]['cuantity']) == 0:
                order_details_obj.delete()
                return HttpResponse({f"{product.name} fue eliminado de la orden"})

        return HttpResponse({"order actualizada con exito"})

class order_detail_view_set(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
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
            return HttpResponse({'Productos duplicados'})

        cuantity_data = request.POST.getlist('order_details.cuantity')

        #validate that cuantities are 1 or more
        for cuantity in cuantity_data:
            if int(cuantity) < 1:
                return HttpResponse({'la cantidad no puede ser menor a 1'})

        #check stock before creating order
        for idx, val in enumerate(products_data):
            product = Product.objects.get(pk = products_data[idx])
            if product.stock < int(cuantity_data[idx]):
                return HttpResponse({f"No hay suficiente stock del producto {product.name}"})

        #this new order will be used to attach products and cuantities
        order =  Order.objects.create()

        #once validations are done details can be attached to the order and cuantity can be substracted from stock
        for idx, val in enumerate(products_data):
            product = Product.objects.get(pk = products_data[idx])
            product.stock = product.stock - int(cuantity_data[idx])
            product.save()
            OrderDetail.objects.create(order = order, cuantity = cuantity_data[idx], product = product)
        
        return HttpResponse({f'orden {order.id} creada'})
