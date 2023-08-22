from django.db import models

class User(models.Model):
    """Model that represents a SoleHub user"""
    uid = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    shoe_size = models.CharField(max_length=5)
    address = models.CharField(max_length=250)
   
   
    