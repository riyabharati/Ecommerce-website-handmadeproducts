from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    Customer,
     Product,
      Cart, 
      OrderPlaced
      )
# Register your models here.


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=['id','user','name','address']
 
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=['id', 'name','selling_price','discounted_price','product_image','category', 'artistname']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product','quantity']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display=['id','user','customer','customer_info','product','product_info','quantity','ordered_date','status']

    def customer_info(self,obj):
        link=reverse('admin:customer_change',args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>',link,obj.customer.name)

    def product_info(self,obj):
        link=reverse('admin:product_change',args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>',link,obj.product.name)


