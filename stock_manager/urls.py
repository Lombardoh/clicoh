from django.urls import path
from stock_manager.views import produt_view_set, order_view_set, order_detail_view_set

product_data_list = produt_view_set.as_view({
    'get': 'list',
    'post': 'create',
})
product_data_detail = produt_view_set.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

order_data_list = order_view_set.as_view({
    'get': 'list',
    'post': 'create',
})

order_data_detail = order_view_set.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

order_data_detail_list = order_detail_view_set.as_view({
    'get': 'custom',
    'post': 'create'
})

urlpatterns = [
    path('products/', product_data_list, name='product_data_list'),         
    path('products/<pk>', product_data_detail, name='product_data_detail'),
    path('orders/', order_data_list, name='order_data_list'),
    path('orders/<pk>', order_data_detail, name='order_data_detail'),
    path('orders/create', order_data_detail_list, name='order-creation'),
    ]