from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator, MinValueValidator

class Customer(User):
    phone = PhoneNumberField(null = True, blank= True)
    age = models.IntegerField( default=18, validators=[MaxValueValidator(50), MinValueValidator(18)])

class Guide(User):
    phone = PhoneNumberField(null = True, blank= True)
    age = models.IntegerField( default=18, validators=[MaxValueValidator(50), MinValueValidator(18)])
    nationality = models.CharField(max_length=100)
    profile_image = models.CharField(max_length=10000, null = True, blank=True)
    image = models.ImageField(upload_to='images/Guide/', null = True, blank=True)
    facebook_url = models.CharField(max_length=1000)
    twitter_url = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)
    language = models.CharField(max_length=100)

# Create your models here.
class Hike(models.Model):    
    LEVEL = [
        ("High", "High"), 
        ("Low", "Low"), 
        ("Medium", "Medium"),
    ]
    description = models.CharField(max_length=1000)
    duration = models.IntegerField(default=1)
    distance = models.IntegerField(default=1)
    group_size = models.IntegerField(default=1)
    trail = models.CharField(max_length=1000)
    address = models.CharField(max_length=100)
    mountain = models.CharField(max_length=100)
    altitude = models.IntegerField(default=1)
    area = models.IntegerField(default=1)
    cost = models.IntegerField(default=1)
    level = models.CharField(max_length=100, choices=LEVEL, default='High')
    hike_date = models.DateField()
    available_capcity = models.IntegerField(default=0)
    gmap_url = models.CharField(max_length=10000)
    user_id = models.ForeignKey(Guide, on_delete= models.CASCADE, null=False)     
    image = models.ImageField(upload_to='images/Hikes/',null = True, blank=True)
    image_name = models.CharField(max_length=500, null = True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class EnrolledHikers(models.Model):
    user = models.ForeignKey(Customer,on_delete=models.CASCADE, null=False)
    hike = models.ForeignKey(Hike,on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'hike',)