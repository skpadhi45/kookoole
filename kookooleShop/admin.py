from csv import list_dialects
from django.contrib import admin
from kookooleShop.models import Categories
from kookooleShop.models import Product
from kookooleShop.models import CustomerPin
from kookooleShop.models import CustomerLogUp
from kookooleShop.models import Order

class AdminCategories(admin.ModelAdmin):
    list_display =['name','image']


class AdminProduct(admin.ModelAdmin):
    list_display =['name','price','category','description','image']




class AdminCustomerLogUp(admin.ModelAdmin):
    list_display =['first_name','last_name','email','phone','pin']



class AdminOrder(admin.ModelAdmin):
   list_display=['status','stock','product','customer' ,'date' ,'quantity','price','cancelation' , 'address','phone']

# Register your models here.
admin.site.register(Categories ,AdminCategories)
admin.site.register(Product ,AdminProduct)
admin.site.register(CustomerLogUp ,AdminCustomerLogUp)
admin.site.register(Order ,AdminOrder)
admin.site.register(CustomerPin)