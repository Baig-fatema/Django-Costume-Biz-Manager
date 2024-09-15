from django.db import models
from django.db import models, IntegrityError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from colorfield.fields import ColorField
# Create your models here.

# Max_purchase Quantity
class Vendor(models.Model):
    full_name=models.CharField(max_length=250,unique=True)
    photo=models.ImageField(upload_to="vendor/",blank=True)
    address=models.TextField(blank=True)
    mobile=models.CharField(max_length=15,unique=True)
    # either you are working with that vendor or not
    status=models.BooleanField(default=False)

    def __str__(self):
        return self.full_name
    
    def clean(self):
        super().clean()
        
        # Check for duplicate full_name and mobile together
        if Vendor.objects.exclude(pk=self.pk).filter(full_name=self.full_name, mobile=self.mobile).exists():
            raise ValidationError({
                'full_name': 'Vendor with this name and mobile number already exists.'
            })

    class Meta:
        verbose_name_plural='1. Vendors'

#customer
class Customer(models.Model) :
    customer_name=models.CharField(max_length=250,unique=True)
    customer_mobile=models.CharField(max_length=15,unique=True)
    customer_address=models.TextField(blank=True)   

    class Meta:
        verbose_name_plural='2. Customers'

    def __str__(self):
        return self.customer_name
    
    def clean(self):
        super().clean()
        
        # Check for duplicate customer_name and customer_mobile together
        if Customer.objects.exclude(pk=self.pk).filter(customer_name=self.customer_name, customer_mobile=self.customer_mobile).exists():
            raise ValidationError({
                'customer_name': 'Customer with this name and mobile number already exists.'
            })
        
# Category (No of Costumes wit title)
class Category(models.Model):
    type=models.CharField(max_length=255,unique=True)
    
    def __str__(self):
        return self.type
    
    class Meta:
        verbose_name_plural='3. Category'
    
# product
class Product(models.Model):
    title=models.CharField(max_length=255)
    detail=models.TextField(blank=True)
    # no of product
    category=models.ForeignKey(Category,on_delete=models.CASCADE)  

    # gender 
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    # change need
    photo=models.ImageField(upload_to="product/",blank=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural='4. Products'
    
#Purchase
class Purchase(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True)
    vendor=models.ForeignKey(Vendor,on_delete=models.SET_NULL,null=True)
    #adding validator that the purchase quantity  should be greater than 0 and less than or equal to avial quantity
    qty=models.IntegerField()
    price=models.FloatField()
    color=ColorField(verbose_name="Color",default='#000000',blank=True)
    total_amt=models.FloatField(editable=False)
    pur_date=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural='5. Purchases'

    def save(self,*args,**kwargs) : 
        self.total_amt=self.qty*self.price
        super(Purchase,self).save()
        # inventory management
        inventory=Inventory.objects.filter(product=self.product).order_by('-id').first()       
        # acessing last row of purchase table
        if inventory:
            totalBal=inventory.total_bal_qty+self.qty
            
        else:
            totalBal=self.qty

        Inventory.objects.create(
            product=self.product,
            purchase=self,
            sale=None,
            purchase_quantity=self.qty,
            sale_quantity=None,
            total_bal_qty=totalBal
        )        

        # Use update_or_create to avoid unique constraint violation
        avail_stock, created = Avail_Stocks.objects.update_or_create(
        Item=self.product,
        category=self.category,
        defaults={
            'qty': totalBal,
            'Item_price': self.price,
            'total_price': self.price * totalBal,
        }
    )

    #on deleting the record dont delelte anything from inventory
    def delete(self, *args, **kwargs):
        # Set related Inventory records' purchase field to NULL
        Inventory.objects.filter(purchase=self).update(purchase=None)
        # Delete the Purchase record
        super(Purchase, self).delete(*args, **kwargs)    


#Avail able Stocks
class Avail_Stocks(models.Model):
    Item=models.ForeignKey(Product,on_delete=models.CASCADE)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,default=0,null=True)
    #count available quantity
    qty=models.IntegerField()
    Item_price=models.FloatField()

    total_price=models.FloatField()
    #color
    color = ColorField(default='#000000', blank=True)  # Add ColorField here
    class Meta:
        verbose_name_plural='7. Stocks'
        unique_together = ('Item', 'category')

    # return avail stocks
    def __int__(self):
        return self.qty

    def __str__(self):
        return f"{self.Item} - {self.category} - {self.color}"    
    
#Sales
class Sales(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True)
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    qty=models.IntegerField(
        validators=[MinValueValidator(0)]
    )
    price=models.FloatField()
    total_amt=models.FloatField(editable=False)
    sale_date=models.DateTimeField(auto_now_add=True)

    #color
    color = ColorField(default='#000000', blank=True)  # Add ColorField here

    # Fields automatically managed by the model
    max_sale_qty = models.IntegerField(editable=False, null=True, blank=True) 

    class Meta:
        verbose_name_plural='6. Sales'

    def get_available_colors(self):
        """
        Returns a queryset of available colors for the given product and category.
        """
        return Avail_Stocks.objects.filter(Item=self.product, category=self.product.category).values_list('color', flat=True).distinct()

    def __str__(self):
        return f"{self.product} - {self.customer} - {self.color}"    
    
    def clean(self):
        super().clean()

        # Validate that the category of the product is available in stock
        try:
            avail_stock = Avail_Stocks.objects.filter(Item=self.product, category=self.category).order_by('-id').first()
            
            # If no stock entry is found for the product and category combination
            if not avail_stock:
                raise ValidationError(f'Product with category "{self.category}" is not available in stock.')

            available_qty = avail_stock.qty
            self.max_sale_qty = available_qty

            if self.qty < 0:
                raise ValidationError({'qty': 'Sale quantity cannot be negative.'})
            if self.qty > available_qty:
                raise ValidationError({'qty': f'Sale quantity cannot be greater than available stock ({available_qty}).'})

        except Avail_Stocks.DoesNotExist:
            raise ValidationError(f'No available stock found for the product "{self.product}" in the selected category "{self.category}".')

    def save(self, *args, **kwargs):
        self.clean()  # Perform model validation
        self.total_amt = self.qty * self.price

        # Save the Sales instance
        super(Sales, self).save(*args, **kwargs)

        # Update Avail_Stocks and Inventory
        avail_stock, created = Avail_Stocks.objects.get_or_create(
            Item=self.product,
            category=self.category,
            defaults={'qty': 0, 'Item_price': self.price, 'total_price': 0}
        )

        if avail_stock:
            avail_stock.qty -= self.qty
            avail_stock.total_price = avail_stock.Item_price * avail_stock.qty
            avail_stock.save()

            # Create Inventory entry
            Inventory.objects.create(
                product=self.product,
                sale=self,
                sale_quantity=self.qty,
                total_bal_qty=avail_stock.qty
            )
    
    #manage inventory records on deleting the sales reocrd
    def delete(self, *args, **kwargs):
        Inventory.objects.filter(sale=self).update(sale=None)
        super(Sales, self).delete(*args, **kwargs)

class Inventory(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    purchase=models.ForeignKey(Purchase,on_delete=models.SET_NULL, null=True)
    sale=models.ForeignKey(Sales,on_delete=models.SET_NULL, null=True)
    # sale_customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    # purchase_vendor=models.ForeignKey(Vendor,on_delete=models.SET_NULL,null=True)
    purchase_quantity=models.IntegerField(default=0,null=True)
    sale_quantity=models.IntegerField(default=0,null=True)
    total_bal_qty=models.IntegerField()
    
    class Meta:
        verbose_name_plural='8. Inventory'
    
    #showing unit
    def product_unit(self):
        return self.product.unit.title
        

    #showing pur_date
    def pur_date(self):
        if self.purchase:
            return self.purchase.pur_date
    
    #showing sale_date
    def sale_date(self):
        if self.sale:
            return self.sale.sale_date
    #showing product category 
    def product_category(self):
        if self.purchase:
            return self.purchase.category.type
        elif self.sale:
            return self.sale.category.type
        return None
    product_category.short_description = 'Product Category'

    # showing vendor
    def purchase_vendor(self):
        if self.purchase:
            return self.purchase.vendor
        return None
    
    # Showing Customer
    def sale_customer(self):
        if self.sale:
            return self.sale.customer
        return None
    