# import imp
from typing import ValuesView
from django.urls import path, re_path
from django.contrib.flatpages import views
from django.urls.resolvers import URLPattern
from .import views 
from django.contrib.flatpages.sitemaps import FlatPageSitemap
from django.contrib.sitemaps.views import sitemap
from django.conf import settings
from django.conf.urls.static import static

app_name = 'customadmin'

urlpatterns = [
    path('',views.user_login,name="login"),
    path('logout/',views.logout_view),
    path('dashboard/',views.dashboard, name='dashboard'),

    path('home/',views.home),

    #User URLs
    path('user/<int:page_size>',views.user, name='user'),
    path('profile/',views.profile),
    path('edit/<int:id>', views.edit, name='edit'),  
    path('update/<int:id>', views.update, name='update'),
    path('delete/<int:id>', views.delete),  



    #Category URLs
    path('category/',views.category, name='category'),
    path('addcategory/',views.addCategory),
    path('editcategory/<int:id>', views.editCategory, name='edit'),  
    path('updatecategory/<int:id>', views.updateCategory, name='update'),
    path('deletecategory/<int:id>', views.deleteCategory),


   #Banner URLs
    path('banner/',views.banner, name='banner'),
    path('addbanner/',views.addBanner),
    path('editbanner/<int:id>', views.editBanner, name='edit'),  
    path('updatebanner/<int:id>', views.updateBanner, name='update'),
    path('deletebanner/<int:id>', views.deleteBanner),

    
    #Order URLs    
    path('order/', views.order, name='order'),
    path('view-order/<int:orderId>', views.view_order),


    #Product Details
    path('product/',views.product, name='product'),
    path('addproducts/',views.addProducts),
    path('editproduct/<int:id>', views.editProduct, name='edit'),  
    path('updateproduct/<int:id>', views.updateProduct, name='update'),  
    path('deleteproduct/<int:id>', views.deleteProduct),  
    
    path('productattr/',views.productAttribute, name='productattr'),
    path('productattrval/',views.productAttributeValues, name='productattrval'),
    path('add-productattr/',views.addProductAttribute),
    path('add-productattrvalue/',views.addProductAttributeValues),


    #Coupon
    path('coupon/',views.coupon, name='coupon'),
    path('addcoupon/',views.addCoupon),
    path('editcoupon/<int:id>', views.editCoupon, name='edit'),  
    path('updatecoupon/<int:id>', views.updateCoupon, name='update'),
    path('deletecoupon/<int:id>', views.deleteCoupon),

    #Contact
    path('contact/',views.contact, name='contact'),
    path('viewcontact/<int:id>',views.viewContact, name='view'),



    #Configuation URLs
    path('configuration/',views.configuration,name='configuration'),
    path('addconfiguration/',views.addConfiguration),
    path('editConfig/<int:id>', views.editConfig, name='edit'),  
    path('updateConfig/<int:id>', views.updateConfig, name='update'),
    path('deleteConfig/<int:id>', views.deleteConfig),

    #Email Template
    path('emailtemplate/',views.emailtemplate,name='emailtemplate'),
    path('addemail/',views.addEmail),
    path('editemailtemplate/<int:id>', views.editEmailTemplate),  
    path('updateEmail/<int:id>', views.updateEmail),
    path('send-mail/<int:contactId>', views.sendMail),

    #Report
    path('report/',views.report,name='report'),
    path('generate-csv/',views.generateCSV),

     path('cms/', views.cms, name="cms"),
    path('addcms/', views.addnewcms, name='addnewcms'),
    path('cmsupdate/<int:id>/', views.cmsupdate, name='cmsupdate'),
    path('cmsdelete/<int:id>/', views.cmsdelete, name='cmsdelete'),
    path('sitemap.xml', sitemap,{'sitemaps': {'flatpages': FlatPageSitemap}}, name='django.contrib.sitemaps.views.sitemap'),

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)