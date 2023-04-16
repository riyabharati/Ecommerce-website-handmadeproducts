from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=200, null=True)
    lastname = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=10, null=True)
    username = models.CharField(max_length=200, null=True)
    email = models.EmailField
    profile_pic = models.FileField(upload_to='static/uploads', default= 'static/images/IMG_20201128_121602.jpg')
    create_date = models.DateTimeField(auto_now_add=True)



