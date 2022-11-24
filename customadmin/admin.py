from django.contrib import admin

from customadmin.models import Banner, Coupon,Category, Order

# Register your models here.
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Coupon)
admin.site.register(Banner)
