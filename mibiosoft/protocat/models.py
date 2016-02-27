from django.db import models
from django.contrib.auth.models import User
# for Protocol
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

'''
This page is to create python classes, which are then converted in to tables for our database
So things like, User, Protocol, Reagents, etc.
'''

class Profile_Info(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	Profile_Image = models.FileField()

class Protocol_Category(models.Model):
	title = models.TextField()
	author = models.ForeignKey(User)
	description = models.TextField()
	parent_category = models.ForeignKey('self', blank=True, null=True)

class Reagent(models.Model):
	name = models.TextField()

class Protocol(models.Model):
	title = models.TextField()
	author = models.ForeignKey(User)
	description = models.TextField()
	# many protocols to one category
	category = models.ForeignKey(Protocol_Category)
	is_searchable = models.BooleanField(default=True)
	upload_date = models.DateField()
	number_of_ratings = models.IntegerField(default=0)
	sum_of_ratings = models.IntegerField(default=0)
	# many branching protocols to one parent protocol
	last_revision = models.ForeignKey('self', blank=True, null=True)
	# many different protocols can use one reagent, one protocol can use many reagents
	reagents = models.ManyToManyField(Reagent)
	# still need to add steps, which could possible be a separate class instead of just text
