from django.db import models
from .user import User

class Product(models.Model):
    name = models.CharField(max_length=50)
    image = models.CharField(max_length=10000)
    description = models.CharField(max_length=50)
    condition = models.CharField(max_length=20)
    price = models.IntegerField()
    color = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    seller_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_info')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_info')
