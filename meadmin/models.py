from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms import IntegerField
from django.db.models.base import Model
from django.db.models.deletion import CASCADE

class Customer(models.Model):
 user=models.ForeignKey(User, on_delete=models.CASCADE)
 name=models.CharField(max_length=200)
 address=models.CharField(max_length=200)

 def __str__(self):
     return str(self.id)

CATEGORY_CHOICES=(
    ('B', 'Birthdaycard'),
    ('L','Lovecard'),
    ('P','Painting'),
    ('S','Sistergift'),
)


class Product(models.Model):
    name = models.CharField(max_length=200)
    selling_price=models.FloatField()
    discounted_price=models.FloatField()
    product_image=models.ImageField(upload_to='productimg')
    category= models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    artistname = models.CharField(max_length=200)
    def __str__(self):
        return self.name


class Cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return str(self.id) 

    @property
    def total_cost(self):
        return self.quantity*self.product.discounted_price

STATUS_CHOICES=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
)

class OrderPlaced(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    ordered_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')

    @property
    def total_cost(self):
        return self.quantity*self.product.discounted_price
    

