from django.db import models

class Product(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=30)
    price = models.FloatField()
    stock = models.IntegerField()
    
    def __str__(self):
        return self.name

class Order(models.Model):
    date_time = models.DateTimeField(auto_now_add=True)


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cuantity = models.IntegerField()