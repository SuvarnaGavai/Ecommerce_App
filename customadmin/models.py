import datetime
from distutils.command.upload import upload
from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.contrib.flatpages.models import FlatPage

from eshop.models import UserAddress


class Category(models.Model):
    id = models.AutoField( primary_key=True)
    name = models.CharField( max_length=30, blank=True)
    created_by = models.CharField( max_length=30, blank=True)
    created_date = models.DateField(auto_now_add=True)
    modify_by = models.CharField( max_length=30, blank=True)
    modify_date = models.DateField(auto_now=True)



class Configuration(models.Model):
    id = models.AutoField( primary_key=True)
    configuration_key = models.CharField( max_length=30, blank=True)
    configuration_value = models.CharField( max_length=30, blank=True)
    created_by = models.CharField( max_length=30, blank=True)
    created_date = models.DateField(auto_now_add=True)
    modify_by = models.CharField( max_length=30, blank=True)
    modify_date = models.DateField(auto_now_add=True)


class Banner(models.Model):
    id = models.AutoField( primary_key=True)
    name = models.CharField( max_length=30, blank=True)
    image = models.ImageField(upload_to='images/')
    sort_id = models.CharField( max_length=30, blank=True)
    created_by = models.ForeignKey(User,related_name='created_by',on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    modify_by = models.ForeignKey(User,related_name='modify_by',on_delete=models.CASCADE)
    modify_date = models.DateField(auto_now_add=True)


class Product(models.Model):
    id = models.AutoField( primary_key=True)
    name = models.CharField( max_length=30, blank=True)
    image = models.ImageField(upload_to='images/')
    price = models.IntegerField(blank=True)
    quantity = models.IntegerField(blank=True)
    brand = models.CharField(max_length=30,blank=True)
    category = models.CharField(max_length=30,blank=True)
    gender = models.CharField(max_length=10,blank=True)

# #Product Details
class ProductAttribute(models.Model):
    id = models.AutoField( primary_key=True)
    name = models.CharField( max_length=30, blank=True)
    created_by = models.CharField( max_length=30, blank=True)
    created_date = models.DateField(auto_now_add=True)
    modify_by = models.CharField( max_length=30, blank=True)
    modify_date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.name

class ProductAttributeValues(models.Model):
    id = models.AutoField( primary_key=True)
    product_attribute_id = models.ForeignKey(ProductAttribute,on_delete=models.CASCADE)
    attribute_value = models.CharField(max_length=45, blank=True)
    created_by = models.CharField(max_length=30, blank=True)
    created_date = models.DateField(auto_now_add=True)
    modify_by = models.CharField(max_length=30, blank=True)
    modify_date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.attribute_value

class ProductAttributesAssociate(models.Model):
    id = models.AutoField( primary_key=True)
    productId = models.ForeignKey(Product,on_delete=models.CASCADE)
    product_attribute_id = models.ForeignKey(ProductAttribute,on_delete=models.CASCADE)
    product_attribute_value = models.ForeignKey(ProductAttributeValues,on_delete=models.CASCADE)


# #Coupons Model
class Coupon(models.Model):
    id = models.AutoField( primary_key=True)
    code = models.CharField( max_length=42, blank=True)
    percent_off = models.FloatField(max_length=12.2, blank=True)
    no_of_uses = models.PositiveIntegerField(max_length=30, blank=True)
    created_by = models.ForeignKey(User,related_name='Coupon_created_by',on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    modify_by = models.ForeignKey(User,related_name='Coupon_modify_by',on_delete=models.CASCADE)
    modify_date = models.DateField(auto_now_add=True)


class Contact(models.Model):
    id = models.AutoField( primary_key=True)
    name = models.CharField( max_length=40, blank=True)
    email = models.CharField( max_length=40, blank=True)
    message = models.CharField( max_length=40, blank=True)
    subject = models.CharField( max_length=40, blank=True)
    created_date = models.DateField(auto_now_add=True)
    modify_by = models.CharField( max_length=30, blank=True)
    modify_date = models.DateField(auto_now_add=True)


class EmailTemplates(models.Model):
    id = models.AutoField( primary_key=True)
    title = models.CharField( max_length=30, blank=True)
    subject = models.CharField( max_length=30, blank=True)
    content = RichTextField(blank=True,null=True)

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    userId = models.ForeignKey(User,on_delete=models.CASCADE)
    shipping_method = models.CharField( max_length=100, blank=True)
    created_date = models.DateField(auto_now_add=True)
    coupon_code = models.ForeignKey(Coupon,on_delete=models.CASCADE,null=True)
    grand_total = models.DecimalField(max_digits=25, decimal_places=2)
    shipping_address = models.ForeignKey(UserAddress,on_delete=models.CASCADE)

class OrderDetails(models.Model):
    id = models.AutoField(primary_key=True)
    orderId = models.ForeignKey(Order,on_delete=models.CASCADE)
    productId = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField( max_length=30, blank=True)
    total = models.DecimalField(max_digits=25, decimal_places=2)


class CMS_Model(FlatPage):
    meta_title = models.TextField(blank=True, null=True)
    meta_desc = models.TextField(blank=True, null=True)
    meta_key = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='CMS_created_by', on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='CMS_modified_by', on_delete=models.CASCADE)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cms"

# class FlatPage(models.Model):
#     url = models.CharField(max_length=100)
#     title = models.CharField(max_length=200)
#     content = models.TextField(blank=True)
#     enable_comments = models.BooleanField(default=False)
#     template_name = models.CharField(max_length=70, blank=True)
#     registration_required = models.BooleanField(default=False)
    