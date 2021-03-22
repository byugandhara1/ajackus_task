from django.db import models
from django.contrib.auth.models import AbstractUser
# from phone_field import PhoneField
# Create your models here.

class User(AbstractUser):

    fullname = models.CharField(max_length=150,null=False,blank=False)
    email = models.EmailField('email address',primary_key=True, unique=True)
    mobile = models.IntegerField(null=True,blank=True)
    address=models.TextField(max_length=300,blank=True,null=True)
    city = models.CharField(max_length=50,blank=True,null=True)
    state = models.CharField(max_length=50,blank=True,null=True)
    country = models.CharField(max_length=50,blank=True,null=True)
    pincode = models.IntegerField(null=True,blank=True)
    is_author=models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Content(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=100,null=False,blank=False)
    body=models.TextField(max_length=300,null=False,blank=False)
    summary=models.TextField(max_length=60,null=False,blank=False)
    pdf = models.FileField(upload_to='pdfs/', null=True, blank=True)
    category=models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.title

