from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from framework.models import BaseModel

class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    avtar  = models.ImageField(upload_to='user_images')
    phone = models.CharField(max_length=20)
    

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Company.objects.create(user=instance)
    instance.profile.save()


class Company(BaseModel):
    user = models.OneToOneField(User,related_name="user_company", on_delete=models.CASCADE)
    comapny_name = models.CharField(max_length=50)
    comapny_address = models.TextField(max_length=200)
    logo  = models.ImageField(upload_to='company_images')
    company_website =  models.CharField(max_length=70) 
    phone = models.CharField(max_length=20)