from unicodedata import decimal
from django.db import models
from django.contrib.auth.models import User



# # Create your models here.


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    userId = models.ForeignKey(User,on_delete=models.CASCADE)
    productId = models.ForeignKey('customadmin.Product',on_delete=models.CASCADE)
    quantity = models.IntegerField( max_length=30, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

class Wishlist(models.Model):
    id = models.AutoField(primary_key=True)
    userId = models.ForeignKey(User,on_delete=models.CASCADE)
    productId = models.ForeignKey('customadmin.Product',on_delete=models.CASCADE)
    

class UserAddress(models.Model):
    id = models.AutoField(primary_key=True)
    userId = models.ForeignKey(User,on_delete=models.CASCADE)
    address1 = models.CharField( max_length=100, blank=True)
    address2 = models.CharField( max_length=100, blank=True)
    city = models.CharField( max_length=45, blank=True)
    state = models.CharField( max_length=45, blank=True)
    country = models.CharField( max_length=45, blank=True)
    zipcode = models.CharField( max_length=45, blank=True)
    is_default = models.BooleanField(default=False, blank=True)

