from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from . import views



app_name = 'eshop'

urlpatterns = [

    path('',views.eshop),
    path('addcontact/',views.addcontactus),
    path('contactus/',views.contactus,name='contactus'),
    path('error/',views.error),
    path('blog/',views.blog),
    path('blog_single/',views.blog_single),
    path('shop/',views.shop),
    path('checkout/',views.checkout),
    path('product_details/',views.product_details),
    path('view_product_details/<int:id>',views.view_product_details),

    path('login/',views.user_login),
    path('logout/',views.logout_view),
    
    path('cart/',views.cart),
    path('cart-operation/<int:productId>/<str:operation>',views.cartOperation),
    path('remove-from-cart/<int:itemId>',views.removeFromCart),
    path('add-user/',views.add_user),
    path('user-address/',views.user_address),

    path('user-profile/',views.user_profile),
    path('edit-profile/',views.edit_profile),
    path('update-profile/',views.update_profile),

    path('change-password/',views.change_password),
    path('change-password-page/',views.change_password_page),

    path('place-order/',views.add_order),

    path('add-address/',views.add_address),
    path('edit-address/<int:id>', views.edit_address),
    path('update-address/<int:id>',views.update_address),
    path('delete-address/<int:id>', views.delete_address),
    path('set-default-address/<int:id>', views.set_address_default),

    path('wishlist/', views.wishlist),
    path('add_wishlist/<int:productId>', views.add_wishlist),
    path('move-to-cart/<int:productId>', views.moveTocart),
    path('remove_wishlist/<int:id>', views.remove_wishlist),
    
    path('review/', views.review),
    
    path('process-payment/<int:orderId>', views.process_payment, name='process_payment'),
    path('payment_done/', views.payment_done, name='payment_done'),
    path('payment_cancelled/', views.payment_canceled, name='payment_cancelled'),

    path('apply-coupon/', views.apply_coupon),

    path("password_reset", views.password_reset_request, name="password_reset"),
    
    path('subscribe/', views.subscription),

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)