from django.db import models
from .order import Order
from .product import Product

class Cart(models.Model):
      """Model that represents a SoleHub user's cart"""
      order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
      product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_products')
