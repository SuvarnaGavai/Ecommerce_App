from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from email.headerregistry import Address
from itertools import product
import json
from urllib import request
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import login ,authenticate,logout
from customadmin.models import Banner, CMS_Model, Configuration, Contact, Coupon, Order, OrderDetails, Product
from .forms import AddressForm, UserProfileForm
from eshop.models import Cart, UserAddress, Wishlist
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.views.generic import TemplateView
from django.views.generic import FormView
from django.urls import reverse
from django.contrib.auth.models import Group
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from decimal import Decimal
from django.core import serializers

from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError


# Create your views here.

#User Add
def add_user(request):
    if request.method == "POST":
        print('Inside')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        my_user = User.objects.create_user(first_name=first_name, last_name=last_name,username=username,email=email,password=password)
        my_user.save()
        admin_group = Group.objects.get(name='user-group') 
        admin_group.user_set.add(my_user)
    return redirect('/eshop/login')




#Update

#Login
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        route = ''
        if 'route' in request.session:
            route = request.session['route']
            items = request.session['items']
            del request.session['route']
        print(route)
        try:
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                if(route != ''):
                    itemList = []
                    for item in items:
                        itemList.append(Cart(productId=Product.objects.get(id = item['product']),quantity = item['quantity'],total = item['total'],userId = request.user))
                    Cart.objects.bulk_create(itemList)
                    del request.session['items']
                    return redirect('/eshop/'+route)
                else:
                    return redirect('/eshop/')
            else:
                print("somthing tried to login and failed")
                print("They used username: {} and password: {}".format(username,password))

                return redirect('/eshop/login')
        except Exception as identifier:
            print('Error :- '+ str(identifier))
            return redirect('/eshop/login')
    else:
        return render(request,'user_login.html')


#Home Page
def eshop(request):
    banners = Banner.objects.all().order_by('sort_id')
    products = Product.objects.all()
    cms = CMS_Model.objects.all()
    mobile = Configuration.objects.get(configuration_key = 'Mobile')
    email = Configuration.objects.get(configuration_key = 'Email')
    if request.user.is_authenticated:
        user = User.objects.get(id = request.user.id)
        itemCount = Cart.objects.filter(userId = user).count
        return render(request, 'index1.html',{'products':products,'cartItemCount':itemCount,'is_login':True,'banners':banners,'cms':cms,'mobile':mobile,'email':email})
    else:
        itemCount = 0
        if 'items' in request.session:
            item_list = request.session['items']
            itemCount = len(item_list)
            print(item_list)
    return render(request, 'index1.html',{'products':products,'cartItemCount':itemCount,'is_login':False,'banners':banners,'cms':cms,'mobile':mobile,'email':email})

def addcontactus(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        contact = Contact(name=name,email=email,subject=subject,message=message)
        contact.save()
        return render(request, 'contact-us.html')
    return render(request, 'contact-us.html')

#Contact Us
def contactus(request):
    cms = CMS_Model.objects.all()
    mobile = Configuration.objects.get(configuration_key = 'Mobile')
    email = Configuration.objects.get(configuration_key = 'Email')
    if request.user.is_authenticated:
        user = User.objects.get(id = request.user.id)
        itemCount = Cart.objects.filter(userId = user).count
        return render(request, 'contact-us.html',{'cartItemCount':itemCount,'is_login':True, 'cms':cms, 'mobile':mobile,'email':email})
    return render(request, 'contact-us.html',{'cartItemCount':0,'is_login':False, 'cms':cms, 'mobile':mobile,'email':email})


def error(request):
    return render(request, '404.html')

def blog_single(request):
    return render(request, 'blog-single.html')

def blog(request):
    return render(request, 'blog.html')

def shop(request):
    products = Product.objects.all()
    cms = CMS_Model.objects.all()
    mobile = Configuration.objects.get(configuration_key = 'Mobile')
    email = Configuration.objects.get(configuration_key = 'Email')
    if request.user.is_authenticated:
        user = User.objects.get(id = request.user.id)
        itemCount = Cart.objects.filter(userId = user).count
        return render(request, 'shop.html',{'products':products,'cartItemCount':itemCount,'is_login':True, 'cms':cms, 'mobile':mobile,'email':email})
    else:
        itemCount = 0
        if 'items' in request.session or request.session['items']:
            item_list = request.session['items']
            itemCount = len(item_list)
            print(item_list)
        return render(request, 'shop.html',{'products':products,'cartItemCount':itemCount,'is_login':False, 'cms':cms, 'mobile':mobile,'email':email})  



def product_details(request):
    cms = CMS_Model.objects.all()
    return render(request, 'product-details.html',{'cms':cms,})

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/eshop/login')
    return redirect('/eshop/login')

def view_product_details(request,id):
    details = Product.objects.get(id=id)
    return render(request, 'product-details.html',{'details':details, 'is_login':True})

@csrf_exempt
def cartOperation(request,productId,operation):
    product = Product.objects.get(id = productId)
    itemCount = 0
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        if Cart.objects.filter(userId=user, productId = product).exists():
            cartItem =  Cart.objects.get(userId= user, productId = product)
            if(operation == 'add'):
                cartItem.quantity += 1
                cartItem.total = cartItem.quantity * cartItem.productId.price
                cartItem.save()
            elif (operation == 'remove'):
                if cartItem.quantity != 1:
                    cartItem.quantity -= 1
                    cartItem.total = cartItem.quantity * cartItem.productId.price
                    cartItem.save()
                else:
                    cartItem.delete()  
        else:
            newItem = Cart(productId = product,userId = user,quantity = 1)
            newItem.total = newItem.productId.price
            newItem.save()
        itemCount = len(Cart.objects.filter(userId = user))
        print(itemCount)
    else:
        if not 'items' in request.session or not request.session['items']:
            
            item = {
                'quantity':1,
                'total':product.price,
                'product':product.id,
            }
            request.session['items'] = [item]
            print(item)
        else:
            isPresent = False
            item_list = request.session['items']
            for i in range(len(item_list)):
                if item_list[i]['product'] == productId:
                    isPresent = True
                    if(operation == 'add'):
                        item_list[i]['quantity'] += 1
                        item_list[i]['total'] = product.price * item_list[i]['quantity']
                    elif(operation == 'remove'):
                        if item_list[i]['quantity'] != 1:
                            item_list[i]['quantity'] -= 1
                            item_list[i]['total'] = product.price * item_list[i]['quantity']
                        else :
                            del item_list[i]
            if not isPresent:
                item = {
                    'quantity':1,
                    'total':product.price,
                    'product':product.id,
                }
                item_list.append(item)
            
            request.session['items'] = item_list
        itemCount = len(request.session['items'])
    data = {
        'itemCount':itemCount
    }
    return JsonResponse(data, safe=False)
    # if(page == 'home'):
    #     return redirect('/eshop')
    # else : 
    #     return redirect('/eshop/cart') 




def removeFromCart(request,itemId):
    print('hi')
    if request.user.is_authenticated:
        item = Cart.objects.get(id = itemId)
        item.delete()
        return redirect('/eshop/cart')
    else:
        return redirect('/eshop/login')



#Show Cart
def cart(request):
    try:
        del request.session['coupon-code']
        del request.session['total']
    except KeyError:
        pass
    
    cms = CMS_Model.objects.all()
    mobile = Configuration.objects.get(configuration_key = 'Mobile')
    email = Configuration.objects.get(configuration_key = 'Email')
    if request.user.is_authenticated:
        user = User.objects.get(id = request.user.id)
        itemList = Cart.objects.filter(userId = user)
        subTotal = sum([item.total for item in itemList])
        total = subTotal
        itemCount = len(itemList)
        return render(request,'cart.html',{'products':itemList,'cartItemCount':itemCount,'subTotal':subTotal,'total':total, 'cms':cms,'mobile':mobile,'email':email})
    else:
        if 'items' in request.session:
            items = request.session['items']
        else:
            items = []
        itemList = []
        for item in items:
            print(item)
            itemList.append(Cart(productId=Product.objects.get(id = item['product']),quantity = item['quantity'],total = item['total']))
        subTotal = sum([item.total for item in itemList])
        total = subTotal
        itemCount = len(itemList)
        return render(request,'cart.html',{'products':itemList,'cartItemCount':itemCount,'subTotal':subTotal,'total':total, 'cms':cms,'mobile':mobile,'email':email})


#User Profile
def user_profile(request):
    cms = CMS_Model.objects.all()
    mobile = Configuration.objects.get(configuration_key = 'Mobile')
    email = Configuration.objects.get(configuration_key = 'Email')
    if request.user.is_authenticated:
        itemCount = Cart.objects.filter(userId = request.user).count
        return render(request, 'user_profile.html',{'userInfo': request.user,'cartItemCount':itemCount, 'cms':cms, 'mobile':mobile,'email':email})
    return render(request, 'user_profile.html',{'userInfo': request.user,'cartItemCount':0, 'cms':cms, 'mobile':mobile,'email':email}) 

    
#Edit Profile
def edit_profile(request):  
    user = User.objects.get(id=request.user.id)  
    editform = UserProfileForm(instance=user)
    return render(request,'edit_profile.html', {'editform':editform})  



#update Address
def update_profile(request):  
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)  
        form = UserProfileForm(request.POST,instance=user)  
        if form.is_valid():
            instance = form.save(commit=False)  
            instance.save()
            return redirect("/eshop/user-profile")  
        return render(request, 'edit_profile.html', {'user': user}) 
    return redirect("/eshop/login")

#User Address
def user_address(request):
    cms = CMS_Model.objects.all()
    mobile = Configuration.objects.get(configuration_key = 'Mobile')
    email = Configuration.objects.get(configuration_key = 'Email')
    if request.user.is_authenticated:
        user = User.objects.get(id = request.user.id)
        addressList = UserAddress.objects.filter(userId = user)
        itemCount = Cart.objects.filter(userId = user).count
        return render(request, 'user_address.html',{'addressList':addressList,'cartItemCount':itemCount, 'cms':cms, 'mobile':mobile,'email':email})
    return redirect('/eshop/login')

#Add Address
def add_address(request):
    if request.method == "POST":
        forms = AddressForm(request.POST)
        user = User.objects.get(id = request.user.id)
        if forms.is_valid():
            address1=forms.cleaned_data['address1']
            address2=forms.cleaned_data['address2']
            city=forms.cleaned_data['city']
            state=forms.cleaned_data['state']
            country=forms.cleaned_data['country']
            zipcode=forms.cleaned_data['zipcode']
            addressCount = UserAddress.objects.filter(userId = user).count()
            if addressCount == 0:
                userAddress = UserAddress(userId=user,address1=address1,address2=address2,city=city,state=state,country=country,zipcode=zipcode,is_default=True)
            else:   
                userAddress = UserAddress(userId=user,address1=address1,address2=address2,city=city,state=state,country=country,zipcode=zipcode)
            userAddress.save()
        return redirect("/eshop/user-address")
    else:
        forms = AddressForm() 
    return render(request, 'add-address.html', {'address':forms})

#Edit Address
def edit_address(request,id):  
    editval = UserAddress.objects.get(id=id)  
    editform = AddressForm(instance=editval)
    return render(request,'edit-address.html', {'editform':editform})  
  
#Update Address
def update_address(request, id):  
    if request.user.is_authenticated:
        upadteaddress = UserAddress.objects.get(id=id) #request.user.id)  
        form = AddressForm(request.POST,instance=upadteaddress )  
        if form.is_valid():
            instance = form.save(commit=False)  
            instance.save()
            return redirect("/eshop/user-address")  
        return render(request, 'edit-address.html', {'editform ': form }) 
    return redirect("/eshop/login")


#delete Address
def delete_address(request,id):  
    address = UserAddress.objects.get(id=id) 
    address.delete() 
    return redirect("/eshop/user-address") 

#Set Address Default
def set_address_default(request,id):  
    user = User.objects.get(id = request.user.id)
    UserAddress.objects.filter(userId = user).update(is_default=False)
    address = UserAddress.objects.get(id=id)
    address.is_default = True
    address.save()
    return redirect("/eshop/user-address") 


def change_password(request):  
    if request.user.is_authenticated:
        if request.method == "POST":
            password = request.POST.get('password')
            confirmPass = request.POST.get('confirmPass')
            user = User.objects.get(id=request.user.id)  
            user.set_password(password)
            user.save()
            print(user.password)
            return redirect("/eshop")  
        return render(request, 'edit_profile.html', {'user': user}) 
    return redirect("/eshop/login")

def change_password_page(request):
    if request.user.is_authenticated:
        return render(request, 'change_password.html')
    return redirect("/eshop/login")

#Add Address
def add_order(request):
    user = User.objects.get(id=request.user.id)  
    itemList = Cart.objects.filter(userId = user)
    grandTotal = sum([item.total for item in itemList])
    address = UserAddress.objects.get(userId = user,is_default=True)
    
    if request.session.get('coupon-code'):
        coupon_code = request.session.get('coupon-code')
        coupon = Coupon.objects.get(code=coupon_code)
        coupon.no_of_uses += 1
        coupon.save()
    else:
        coupon = None
    order = Order(userId = user,shipping_address=address,grand_total=grandTotal,shipping_method="online",coupon_code=coupon)
    order.save()
    for item in itemList:
        OrderDetails(orderId=order,quantity=item.quantity,total=item.total,productId=item.productId).save()
    itemList.delete()
    return redirect("/eshop/process-payment/"+str(order.id))
    # process-payment/<int:orderId>
    # return render(request,'cart.html',{'products':[],'cartItemCount':0,'grandTotal':0})



def add_wishlist(request,productId):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        product = Product.objects.get(id = productId)
        if not (Wishlist.objects.filter(userId=user, productId = product).exists()):
            newItem = Wishlist(productId = product,userId = user)
            newItem.save()
            return redirect('/eshop')    
    else:
        return redirect('/eshop/login')


def wishlist(request):
    cms = CMS_Model.objects.all()
    mobile = Configuration.objects.get(configuration_key = 'Mobile')
    email = Configuration.objects.get(configuration_key = 'Email')
    if request.user.is_authenticated:
        itemList = Cart.objects.filter(userId = request.user)
        itemCount = len(itemList)
        wishList = Wishlist.objects.filter(userId=request.user)
        return render(request, 'wishlist.html',{'wishList':wishList,'cartItemCount':itemCount,'cms':cms, 'mobile':mobile,'email':email })
    return redirect("/eshop/login") 

def moveTocart(request,productId):
    user = User.objects.get(id=request.user.id)
    product = Product.objects.get(id = productId)
    if not Cart.objects.filter(userId=user, productId = product).exists():
        newItem = Cart(productId = product,userId = user,quantity = 1)
        newItem.total = newItem.productId.price
        newItem.save()
    wishListItem = Wishlist.objects.get(userId=user, productId = product)
    wishListItem.delete()
    return redirect("/eshop/wishlist") 

#Remove Product from Wishlist
def remove_wishlist(request,id):  
    product = Wishlist.objects.get(id=id) 
    product.delete() 
    return redirect("/eshop/wishlist") 


def review(request):
    itemList = Cart.objects.filter(userId = request.user)
    itemCount = len(itemList)
    mobile = Configuration.objects.get(configuration_key = 'Mobile')
    email = Configuration.objects.get(configuration_key = 'Email')
    if request.user.is_authenticated:
        address = UserAddress.objects.get(userId = request.user,is_default=True)
        return render(request,'review.html',{'products':itemList,'cartItemCount':itemCount, 'is_login':True, 'address':address, 'mobile':mobile,'email':email})
    return render(request,'review.html',{'products':itemList,'cartItemCount':0, 'is_login':False, 'address':address, 'mobile':mobile,'email':email})
    


def checkout(request):
    cms = CMS_Model.objects.all()
    mobile = Configuration.objects.get(configuration_key = 'Mobile')
    email = Configuration.objects.get(configuration_key = 'Email')
    if request.user.is_authenticated:
        itemList = Cart.objects.filter(userId = request.user)
        itemCount = len(itemList)
        address = UserAddress.objects.get(userId = request.user,is_default=True)
        return render(request, 'checkout.html',{'address':address,'cartItemCount':itemCount, 'is_login':True, 'cms':cms,'mobile':mobile,'email':email})
    else :
        request.session['route'] = 'cart'
        return redirect('/eshop/login')




def process_payment(request,orderId):
    # order_id = request.session.get('order_id')
    order = Order.objects.get(id=orderId)
    host = request.get_host()
    if request.session.get('total'):
        total = request.session.get('total')
    else:
        total = order.grand_total
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % total,
        'item_name': 'Order {}'.format(order.id),
        'invoice': str(order.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,reverse('paypal-ipn')),
        # 'return_url': 'http://{}{}'.format(host,reverse('payment_done')),
        # 'cancel_return': 'http://{}{}'.format(host,reverse('payment_cancelled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'process_payment.html', {'order': order, 'form': form})


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def payment_done(request):
    return render(request, 'paypal_success.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'paypal_cancel.html')

def apply_coupon(request):
    if request.user.is_authenticated:
        coupon_code = request.POST.get('couponCode')
        try:
            coupon = Coupon.objects.get(code=coupon_code)
        except Coupon.DoesNotExist:
            coupon = None
        if coupon is not None:
            itemList = Cart.objects.filter(userId = request.user)
            subTotal = sum([item.total for item in itemList])
            print(coupon.percent_off,type(coupon.percent_off))
            print(subTotal,type(subTotal))
            total = float(subTotal) -( float(subTotal) * (coupon.percent_off / 100))
            itemCount = len(itemList)

            request.session['coupon-code']=coupon_code
            request.session['total']=total
            return render(request,'cart.html',{'products':itemList,'cartItemCount':itemCount,'subTotal':subTotal,'total':total})
        return redirect('/eshop/cart')        
    return redirect('/eshop/login')    



def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, settings.EMAIL_HOST_USER , ['bhavsar9421@gmail.com'], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password_reset.html", context={"password_reset_form":password_reset_form})






# Mailchimp Settings
api_key = settings.MAILCHIMP_API_KEY
server = settings.MAILCHIMP_DATA_CENTER
list_id = settings.MAILCHIMP_EMAIL_LIST_ID


# Subscription Logic
def subscribe(email):
    """
     Contains code handling the communication to the mailchimp api
     to create a contact/member in an audience/list.
    """
    mailchimp = Client()
    mailchimp.set_config({
        "api_key": api_key,
        "server": server,
    })

    member_info = {
        "email_address": email,
        "status": "subscribed",
    }

    try:
        response = mailchimp.lists.add_list_member(list_id, member_info)
        print("response: {}".format(response))
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))


def subscription(request):
    if request.method == "POST":
        email = request.POST['email']
        print(email)
        subscribe(email)                
        # messages.success(request, "Email received. thank You! ") # message

    return redirect('/eshop')