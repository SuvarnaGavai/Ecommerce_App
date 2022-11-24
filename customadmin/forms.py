
from django import forms
from django.contrib.auth.models import User
from django.views.generic import CreateView
from ckeditor.widgets import CKEditorWidget
# from ecommerce.customadmin.views import productDe
from .models import Banner, CMS_Model,  Category, Configuration, Contact, Coupon, EmailTemplates, Product, Order, ProductAttribute, ProductAttributeValues, ProductAttributesAssociate
# from .models import Login
from django.forms import modelformset_factory


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'password', 'is_active', 'date_joined')
        widgets = {
            'password': forms.PasswordInput()
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('id', 'name', 'created_by', 'modify_by')


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('id', 'userId', 'shipping_method',
                  'grand_total', 'shipping_address')


class ConfigurationForm(forms.ModelForm):
    class Meta:
        model = Configuration
        fields = ('id', 'configuration_key',
                  'configuration_value', 'created_by', 'modify_by')


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ('id', 'name', 'image', 'sort_id', 'created_by', 'modify_by')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('id', 'name', 'image', 'price',
                  'quantity', 'brand', 'category', 'gender')

ProductAttributesAssociateFormset = modelformset_factory(
    ProductAttributesAssociate,
    fields=('product_attribute_id', 'product_attribute_value'),
    extra=2,
    
)


class ProductAttributeForm(forms.ModelForm):
    class Meta:
        model = ProductAttribute
        fields = ('id', 'name')


class ProductAttributeValueForm(forms.ModelForm):
    class Meta:
        model = ProductAttributeValues
        fields = ('id', 'product_attribute_id', 'attribute_value')

class ProductAttributesAssociateForm(forms.ModelForm):
    class Meta:
        model = ProductAttributesAssociate
        fields = ('id', 'product_attribute_id', 'product_attribute_value')


class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ('id', 'code', 'percent_off',
                  'created_by', 'modify_by', 'no_of_uses')


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('id', 'name', 'email', 'modify_by')


class EmailForm(forms.ModelForm):
    class Meta:
        model = EmailTemplates
        fields = ('id', 'title', 'subject', 'content')

# class CMSForm(forms.ModelForm):
#     class Meta:
#         model = CMS
#         fields = ('id','title','content','meta_title','meta_description','created_by','modify_by')


class CMSForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = CMS_Model
        fields = ['url', 'title', 'content', 'sites', 'meta_title',
                  'meta_desc', 'meta_key', 'created_by', 'modified_by']
        widgets = {
            'url': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'meta_title': forms.TextInput(attrs={'class': 'form-control'}),
            'meta_desc': forms.TextInput(attrs={'class': 'form-control'}),
            'meta_key': forms.TextInput(attrs={'class': 'form-control'}),
            'created_by': forms.Select(attrs={'class': 'form-control'}),
            'modified_by': forms.Select(attrs={'class': 'form-control'}),

        }
