from ast import Index
import csv
from collections import UserList
from email import message_from_bytes, message_from_file
from multiprocessing import context
from traceback import print_exc
from django.http import HttpResponse, HttpResponseRedirect
# from typing import Generic, OrderedDict
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.hashers import make_password
from django.forms import modelformset_factory

from django.contrib.auth.models import Group


from django.conf import settings
from django.core.mail import send_mail
# Create your views here.

from django.template import loader
from django.contrib import messages

from .forms import BannerForm, CMSForm,  ConfigurationForm, CouponForm, EmailForm, ProductAttributeForm, ProductAttributeValueForm, ProductAttributesAssociateForm, ProductAttributesAssociateFormset,  ProductForm, UserForm
from .forms import CategoryForm
from .models import Banner, CMS_Model, Category, Configuration, Contact, EmailTemplates, OrderDetails, ProductAttribute, ProductAttributeValues, ProductAttributesAssociate
from .models import Product, Order, Coupon


def home(request):
    return render(request, 'dashboard.html')


def dashboard(request):
    if request.user.is_authenticated and request.user.groups.filter(name = 'admin-group').exists():
        return render(request, 'index.html')
    return redirect('/customadmin')


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            superuser = authenticate(username=username, password=password)
            if superuser is not None:
                login(request, superuser)
                return redirect('/customadmin/dashboard')

            else:
                print("somthing tried to login and failed")
                print("They used username: {} and password: {}".format(
                    username, password))

                return render(request, 'login.html')
        except Exception as identifier:
            print('Error :- ' + str(identifier))
            return redirect('/customadmin')
    else:
        # print("in else")
        return render(request, 'login.html')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/customadmin')
    return redirect('/customadmin')

# User CRUD

# add user


def profile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            forms = UserForm(request.POST)
            if forms.is_valid():
                password = request.POST.get("password")
                user = forms.save(commit=False)
                user.password = make_password(password)
                user.save()
                #User Added to group
                admin_group = Group.objects.get(name='admin-group') 
                admin_group.user_set.add(user)
                messages.success(request, 'User Added Successfully')
                return redirect("/customadmin/user/2")
            else:
                messages.error(request, 'Problem ouccured while adding user')
        else:
            forms = UserForm()
        return render(request, 'profile.html', {'profile': forms})
    return redirect('/customadmin')

# show users


def user(request,page_size):
    if request.user.is_authenticated:
        # print(request.user.username)
        user_list = User.objects.all().order_by('id')
        page = request.GET.get('page', 1)
        paginator = Paginator(user_list, page_size)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        return render(request, 'user.html', {'users': users})
    return redirect('/customadmin')

# edit user


def edit(request, id):
    if request.user.is_authenticated:
        editval = User.objects.get(id=id)
        form = UserForm(instance=editval)
        return render(request, 'edit.html', {'userform': form})
    return redirect('/customadmin')

# Contact


def viewContact(request, id):
    contact = Contact.objects.get(id=id)
    return render(request, 'view_contact.html', {'contact': contact})


# update user
def update(request, id):
    if request.user.is_authenticated:
        user = User.objects.get(id=id)
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect("/customadmin/user/2")
        return render(request, 'edit.html', {'user': user})
    return redirect("/customadmin")

# delete user


def delete(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect("/customadmin/user/2")


# Category CRUD

# category home
def category(request):
    if request.user.is_authenticated:
        categorie_list = Category.objects.all().order_by('id')
        page = request.GET.get('page', 1)
        paginator = Paginator(categorie_list, 2)
        try:
            categories = paginator.page(page)
        except PageNotAnInteger:
            categories = paginator.page(1)
        except EmptyPage:
            categories = paginator.page(paginator.num_pages)
        return render(request, 'category.html', {'categories': categories})
    return redirect("/customadmin")

# add category


def addCategory(request):
    print(request.method)
    if request.method == "POST":
        forms = CategoryForm(request.POST)
        if forms.is_valid():
            category = forms.save()
            category.save()
            messages.success(request, 'Category Added Successfully')
            return redirect("/customadmin/category")
        else:
            messages.error(request, 'Problem ouccured while adding user')

    else:
        forms = CategoryForm()
    return render(request, 'add_category.html', {'category': forms})


# edit category
def editCategory(request, id):
    category = Category.objects.get(id=id)
    catgoryForm = CategoryForm(instance=category)
    return render(request, 'edit_category.html', {'categoryform': catgoryForm})

# update category


def updateCategory(request, id):
    category = Category.objects.get(id=id)
    form = CategoryForm(request.POST, instance=category)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect("/customadmin/category")
    return render(request, 'edit_category.html', {'categoryform': form})

# delete category


def deleteCategory(request, id):
    category = Category.objects.get(id=id)
    category.delete()
    return redirect("/customadmin/category")

# Order


def order(request):
    orders = Order.objects.all().order_by('id')
    return render(request, 'order.html', {'orders': orders})

def view_order(request,orderId):
    order = Order.objects.get(id=orderId)
    orderDetails = OrderDetails.objects.filter(orderId=orderId)
    return render(request, 'view_order.html',{'order':order,'orderDetails':orderDetails})


# Banner

# Banner home
def banner(request):
    if request.user.is_authenticated:
        banner_list = Banner.objects.all().order_by('id')
        page = request.GET.get('page', 1)
        paginator = Paginator(banner_list, 2)
        try:
            banners = paginator.page(page)
        except PageNotAnInteger:
            banners = paginator.page(1)
        except EmptyPage:
            banners = paginator.page(paginator.num_pages)
        return render(request, 'banner.html', {'banners': banners})
    return redirect("/customadmin")


# Add New Banner
def addBanner(request):
    print(request.method)
    if request.method == "POST":
        forms = BannerForm(request.POST, request.FILES)
        if forms.is_valid():
            banner = forms.save()
            banner.save()
            messages.success(request, 'Banner Added Successfully')
            return redirect("/customadmin/banner")

        else:
            messages.error(request, 'Problem ouccured while adding Banner')

    else:
        forms = BannerForm()
    return render(request, 'add_banner.html', {'banner': forms})


# Edit Banner
def editBanner(request, id):
    banner = Banner.objects.get(id=id)
    bannerForm = BannerForm(instance=banner)
    return render(request, 'edit_banner.html', {'bannerform': bannerForm})

# Update Banner


def updateBanner(request, id):
    banner = Banner.objects.get(id=id)
    form = BannerForm(request.POST, instance=banner)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect("/customadmin/banner")
    return render(request, 'edit_banner.html', {'bannerform': form})

# delete category


def deleteBanner(request, id):
    banner = Banner.objects.get(id=id)
    banner.delete()
    return redirect("/customadmin/banner")


# Product Details
def product(request):
    if request.user.is_authenticated:
        product_list = Product.objects.all().order_by('id')
        page = request.GET.get('page', 1)
        paginator = Paginator(product_list, 4)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        return render(request, 'product.html', {'products': products})
    return redirect("/customadmin")

# Add New Products


def addProducts(request):
    if request.method == "POST":
        forms = ProductForm(request.POST, request.FILES)
        formset = ProductAttributesAssociateForm(request.POST)
        # formset.extra_forms=0
        if forms.is_valid() and formset.is_valid():
            product = forms.save()
            product.save()
            # for form in formset:
            attribute = formset.save(commit=False)
            attribute.productId = product
            attribute.save()
            messages.success(request, 'Product Added Successfully')
            return redirect("/customadmin/product")
        else:
            messages.error(request, 'Problem ouccured while adding product')

    else:
        forms = ProductForm()
        formset = ProductAttributesAssociateForm()
    return render(request, 'add_products.html', {'product': forms, 'formset': formset})

# Edit Product


def editProduct(request, id):
    product = Product.objects.get(id=id)
    attributes = ProductAttributesAssociate.objects.get(productId=product)
    formset = ProductAttributesAssociateForm(instance=attributes)
    productForm = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'productform': productForm, 'formset': formset})

# Update Product


def updateProduct(request, id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=id)
        form = ProductForm(request.POST, instance=product)
        attributes = ProductAttributesAssociate.objects.get(
            productId=product)
        formset = ProductAttributesAssociateForm(request.POST,instance=attributes)
        if form.is_valid() and formset.is_valid():
            product = form.save()
            product.save()
            attribute = form.save(commit=False)
            attribute.productId = product
            attribute.save()
            return redirect("/customadmin/product")
        return render(request, 'edit_product.html', {'productform': form, 'formset': formset})
    return redirect('/customadmin')

# delete Product


def deleteProduct(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect("/customadmin/product")


def productAttribute(request):
    atrribute = ProductAttribute.objects.all().order_by('id')
    return render(request, 'productattr.html', {'productattrs': atrribute})


def productAttributeValues(request):
    atrributeval = ProductAttributeValues.objects.all().order_by('id')
    return render(request, 'productattrval.html', {'productattrsval': atrributeval})


def addProductAttribute(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ProductAttributeForm(request.POST)
            if form.is_valid():
                product_attribute = form.save()
                product_attribute.created_by = request.user.username
                product_attribute.modify_by = request.user.username
                product_attribute.save()
                return redirect("/customadmin/productattr")
        else:
            form = ProductAttributeForm()
        return render(request, 'add_products_attribute.html', {'form': form})
    return redirect('/customadmin')


def addProductAttributeValues(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ProductAttributeValueForm(request.POST)
            if form.is_valid():
                product_attribute_value = form.save()
                product_attribute_value.created_by = request.user.username
                product_attribute_value.modify_by = request.user.username
                product_attribute_value.save()
                return redirect("/customadmin/productattrval")
        else:
            form = ProductAttributeValueForm()
        return render(request, 'add_products_attr_value.html', {'form': form})
    return redirect('/customadmin')


# Coupon CRUD
def coupon(request):
    if request.user.is_authenticated:
        coupon_list = Coupon.objects.all().order_by('id')
        page = request.GET.get('page', 1)
        paginator = Paginator(coupon_list, 5)
        try:
            coupons = paginator.page(page)
        except PageNotAnInteger:
            coupons = paginator.page(1)
        except EmptyPage:
            coupons = paginator.page(paginator.num_pages)
        return render(request, 'coupon.html', {'coupons': coupons})
    return redirect('/customadmin')


# Add New Coupon
def addCoupon(request):
    print(request.method)
    if request.method == "POST":
        forms = CouponForm(request.POST)
        if forms.is_valid():
            coupon = forms.save()
            coupon.save()
            messages.success(request, 'coupon Added Successfully')
            return redirect("/customadmin/coupon")
        else:
            messages.error(request, 'Problem ouccured while adding coupon')
    else:
        forms = CouponForm()
    return render(request, 'add_coupon.html', {'coupon': forms})

# Edit Coupon


def editCoupon(request, id):
    coupon = Coupon.objects.get(id=id)
    couponForm = CouponForm(instance=coupon)
    return render(request, 'edit_coupon.html', {'couponform': couponForm})

# Update Coupon


def updateCoupon(request, id):
    coupon = Coupon.objects.get(id=id)
    form = CouponForm(request.POST, instance=coupon)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect("/customadmin/coupon")
    return render(request, 'edit_coupon.html', {'couponform': form})

# delete coupon


def deleteCoupon(request, id):
    coupon = Coupon.objects.get(id=id)
    coupon.delete()
    return redirect("/customadmin/coupon")

# Contact Us

# Contact Us Home


def contact(request):
    if request.user.is_authenticated:
        contact_list = Contact.objects.all().order_by('id')
        page = request.GET.get('page', 1)
        paginator = Paginator(contact_list, 2)
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        return render(request, 'contact.html', {'contacts': contacts})
    return redirect("/customadmin")
    # contacts = Contact.objects.all().order_by('id')
    # return render(request,'contact.html',{'contacts':contacts})


# Email Template

def emailtemplate(request):
    if request.user.is_authenticated:
        template_list = EmailTemplates.objects.all().order_by('id')
        page = request.GET.get('page', 1)
        paginator = Paginator(template_list, 1)
        try:
            emailtemplates = paginator.page(page)
        except PageNotAnInteger:
            emailtemplates = paginator.page(1)
        except EmptyPage:
            emailtemplates = paginator.page(paginator.num_pages)
        return render(request, 'email_template.html', {'emailtemplates': emailtemplates})
    return redirect("/customadmin")


# Edit Email Template
def editEmailTemplate(request, id):
    emailtemplate = EmailTemplates.objects.get(id=id)
    emailForm = EmailForm(instance=emailtemplate)
    return render(request, 'email_template_edit.html', {'emailForm': emailForm})

# update category


def updateEmail(request, id):
    email = EmailTemplates.objects.get(id=id)
    form = EmailForm(request.POST, instance=email)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect("/customadmin/emailtemplate")
    return render(request, 'email_template_edit.html', {'emailForm': form})


# Add New Email
def addEmail(request):
    print(request.method)
    if request.method == "POST":
        forms = EmailForm(request.POST)
        if forms.is_valid():
            email = forms.save()
            email.save()
            return redirect("/customadmin/emailtemplate")
    else:
        forms = EmailForm()
    return render(request, 'add_email_template.html', {'emailForm': forms})

# Configuration

# Configuartion home
def configuration(request):
    configurations = Configuration.objects.all().order_by('id')
    return render(request, 'configuration.html', {'configurations': configurations})

# add New Configuration


def addConfiguration(request):
    print(request.method)
    if request.method == "POST":
        forms = ConfigurationForm(request.POST)
        if forms.is_valid():
            configuration = forms.save()
            configuration.save()
            messages.success(request, 'Added Successfully')
            return redirect("/customadmin/configuration")
        else:
            messages.error(request, 'Problem ouccured while adding')
    else:
        forms = ConfigurationForm()
    return render(request, 'add_configuration.html', {'configuration': forms})


# edit Configuration
def editConfig(request, id):
    configuration = Configuration.objects.get(id=id)
    configForm = ConfigurationForm(instance=configuration)
    return render(request, 'edit_configuratiom.html', {'configform': configForm})


# update Configuration
def updateConfig(request, id):
    configuration = Configuration.objects.get(id=id)
    form = ConfigurationForm(request.POST, instance=configuration)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect("/customadmin/configuration")
    return render(request, 'edit_configuration.html', {'configform': form})


# delete configuration
def deleteConfig(request, id):
    configuration = Configuration.objects.get(id=id)
    configuration.delete()
    return redirect("/customadmin/configuration")


def report(request):
    orderReportData = []
    userList = User.objects.all()
    for user in userList:
        orderList = Order.objects.filter(userId=user)
        total = sum([item.grand_total for item in orderList])
        orderReportData.append({
            'Email': user.email,
            'ourderCount': len(orderList),
            'total': total,
        })
    return render(request, 'report.html', {'userOrderData': orderReportData})


def generateCSV(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="file.csv"'
    writer = csv.writer(response)
    # print(request.session['data'])
    orderReportData = []
    userList = User.objects.all()
    for user in userList:
        orderList = Order.objects.filter(userId=user)
        total = sum([item.grand_total for item in orderList])
        orderReportData.append({
            'Email': user.email,
            'ourderCount': len(orderList),
            'total': total,
        })
    for orderData in orderReportData:
        writer.writerow(
            [orderData['Email'], orderData['ourderCount'], orderData['total']])
    return response

def sendMail(request,contactId):
    contact = Contact.objects.get(id = contactId)
    subject = 'Support Team Reply'
    message = request.POST.get("paragraph_text")
    print(message)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [contact.email, ]
    send_mail( subject, message, email_from, recipient_list )
    return redirect('/customadmin/contact')


# New Cms
def cms(request):
    cms = CMS_Model.objects.all()
    return render(request, 'cms.html', {'cms': cms})


def addnewcms(request):
    if request.method == 'POST':
        formk = CMSForm(request.POST)
        print(formk.is_valid())
        if formk.is_valid():
            formk.save()
            messages.success(request, 'User Added Successfully')
            return redirect("/customadmin/cms")
        else:
            messages.error(request, 'Problem ouccured while adding user')

    else:
        formk = CMSForm()
        return render(request, 'cmsadd.html', {'cms': cms, 'formk': formk})


def cmsupdate(request, id):
    cms = CMS_Model.objects.get(id=id)
    formk = CMSForm(instance=cms)
    if request.method == 'POST':
        formk = CMSForm(request.POST, request.FILES, instance=cms)
        print(formk.is_valid())
        if formk.is_valid():
            formk.save()
            return redirect('/customadmin/cms')
    else:
        formk = CMSForm(instance=cms)
    return render(request, 'cmsedit.html', {'cms': cms, 'formk': formk})


def cmsdelete(request, id):
    cms = CMS_Model.objects.get(id=id)
    cms.delete()
    return redirect('/cms')
