from django.db import models
from .user import User

class Order(models.Model):
    """Model that represents a order"""
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField()
    payment_type = models.CharField(max_length=10)
    