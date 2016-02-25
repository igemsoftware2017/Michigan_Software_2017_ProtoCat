from django.db import models
from django.contrib.auth.models import User

class Profile_Info(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	Profile_Image = models.FileField()

# Create your models here.
'''
This page is to create python classes, which are then converted in to tables for our database
So things like, User, Protocol, Reagents, etc.
'''
