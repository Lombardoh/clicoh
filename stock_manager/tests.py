from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import include, path, reverse
from rest_framework.test import APITestCase


class OrderViewsTest(APITestCase):
    urlpatterns = [
        path('api/', include('stock_manager.urls')),
    ]

    def test_orders_view(self):
        url = reverse('order_data_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_products_view(self):
        url = reverse('product_data_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_orders_creation_view(self):
        url = reverse('order-creation')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

