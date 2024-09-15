from django.contrib import admin
from .models import Vendor,Customer,Category,Product,Purchase,Sales,Inventory,Avail_Stocks
# Register your models here.
admin.site.site_header = 'Costume Management'
admin.site.site_title="Welcome To Costume Management Panel."

#Vendor
class VendorAdmin(admin.ModelAdmin):
    search_fields=['full_name']
    list_display=["full_name","mobile"]

admin.site.register(Vendor,VendorAdmin)

#Customer
class CustomerAdmin(admin.ModelAdmin):
    search_fields=['customer_name']
    list_display=["customer_name","customer_mobile","customer_address"]
admin.site.register(Customer,CustomerAdmin)

#Category 
admin.site.register(Category)

class ProductAdmin(admin.ModelAdmin):
    search_fields=['title',"category__type"]
    list_display=["title","category"]


admin.site.register(Product,ProductAdmin)

#purchase
class PurchaseAdmin(admin.ModelAdmin):
    search_fields=['product__title','category']
    list_display=["id","product","category","qty","price","total_amt","vendor","pur_date"]

admin.site.register(Purchase,PurchaseAdmin)

#Sales
class SaleAdmin(admin.ModelAdmin):
    search_fields=['product__title','category']
    list_display=["id","product","category","qty","price","total_amt","customer","sale_date"]

admin.site.register(Sales,SaleAdmin)

#Avail_Stocks
class Avail_StocksAdmin(admin.ModelAdmin):
    search_fields=['Item__titel','category__type']
    list_display=['Item','category','qty','Item_price','total_price']

admin.site.register(Avail_Stocks,Avail_StocksAdmin)    

#inventory 
class InventoryAdmin(admin.ModelAdmin):
    search_fields=['product__title']
    list_display=["product","purchase_quantity","purchase_vendor","sale_quantity","sale_customer","total_bal_qty","product_category","pur_date","sale_date"]

admin.site.register(Inventory,InventoryAdmin)


