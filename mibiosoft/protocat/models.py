from django.db import models
from django.contrib.auth.models import User
# for Protocol
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

'''
This page is to create python classes, which are then converted in to tables for our database
So things like, User, Protocol, Reagents, etc.
'''

class ProfileInfo(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	profile_image = models.FileField(null=True, blank=True)
	def __str__(self):
		return str(self.user)
	def email(self):
		return self.user.email
	def is_admin(self):
		return self.user.is_staff
	def date_joined(self):
		return self.user.date_joined

class Category(models.Model):
	title = models.TextField()
	author = models.ForeignKey(User)
	description = models.TextField()
	parent_category = models.ForeignKey('self',
										blank=True,
										null=True)
	def __str__(self):
		return self.title


class Reagent(models.Model):
	name = models.TextField()
	website = models.URLField(null=True, blank=True)
	def __str__(self):
		return self.name

class Protocol(models.Model):
	title = models.TextField()
	author = models.ForeignKey(User)
	description = models.TextField()

	# Allow the revisionist to describe changes made
	change_log = models.TextField()

	# many protocols to one category
	category = models.ForeignKey(Category)

	is_searchable = models.BooleanField(default=True)
	upload_date = models.DateTimeField(auto_now_add=True)

	number_of_ratings = models.IntegerField(default=0)
	sum_of_ratings = models.IntegerField(default=0)

	# many branching protocols to one parent protocol
	last_revision = models.ForeignKey('self',
										blank=True,
										null=True)

	# still need to add steps, which could possible be a separate class instead of just text
	def __str__(self):
		return self.title
	def all_reagents(self):
		return ReagentForProtocol.objects.filter(associated_protocol = self)
	def all_steps(self):
		return BasicStep.objects.filter(protocol = self)

# many ReagentForProtocols for each protocol
class ReagentForProtocol(models.Model):
	amount = models.DecimalField(max_digits=100, decimal_places=5)

	# (L, mL, g, kg, M), might be better if we had a list of these stored
	unit = models.CharField(max_length = 10)

	# link it and other of the same type to the right protocol
	associated_protocol = models.ForeignKey(Protocol)

	reagent = models.ForeignKey(Reagent)

	def __str__(self):
		return str(self.amount) + self.unit + " " + str(self.reagent)

class ProtocolStep(models.Model):
	# required fields
	action = models.TextField()

	# optional fields
	time = models.IntegerField(blank = True, null = True)

	step_number = models.IntegerField()
	protocol = models.ForeignKey(Protocol)

	# link the step to the correct reagents
	associated_reagents = models.ManyToManyField(ReagentForProtocol)

	def __str__(self):
		result = "(" + str(self.protocol) + ") Step " + str(self.step_number)
		if self.time:
			result = result + " for " + str(self.time) + " seconds"
		return result
