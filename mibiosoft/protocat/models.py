from django.db import models
from django.contrib.auth.models import User
# added
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

'''
This page is to create python classes, which are then converted in to tables for our database
So things like, User, Protocol, Reagents, etc.
'''

class ProfileInfo(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	profile_image = models.FileField(blank = True, null = True)
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
	parent_category = models.ForeignKey('self', blank = True, null = True)
	def __str__(self):
		return self.title


class Reagent(models.Model):
	name = models.TextField()
	picture = models.FileField(blank = True, null = True)
	website = models.URLField(blank = True, null = True)
	def __str__(self):
		return self.name
	def get_website(self):
		return self.website

class Protocol(models.Model):
	title = models.TextField()
	author = models.ForeignKey(User)
	description = models.TextField()
	notes = models.TextField(blank = True, null = True)

	# Allow the revisionist to describe changes made
	change_log = models.TextField()

	# many protocols to one category
	category = models.ForeignKey(Category)

	# True if the author want dynamic scaling of products and reactants
	scaleable = models.BooleanField(default = False)
	searchable = models.BooleanField(default = True)

	upload_date = models.DateTimeField(auto_now_add = True)

	# many branching protocols to one parent protocol
	last_revision = models.ForeignKey('self', blank = True, null = True)

	# still need to add steps, which could possible be a separate class instead of just text
	def __str__(self):
		return self.title
	def get_reagents(self):
		return str(ReagentForProtocol.objects.filter(protocol = self))
	def get_steps(self):
		return str(ProtocolStep.objects.filter(protocol = self))
	def get_category(self):
		return str(self.category)
	def is_searchable(self):
		return self.searchable
	def is_scaleable(self):
		return self.scaleable

# many ReagentForProtocols for each protocol
class ReagentForProtocol(models.Model):
	# 1 denotes isFiller, 2 denotes isConstant, and 3 denotes isLinear for
	# scaling of the amounts.
	scaling_type = models.IntegerField(default = 2)

	# 1 denotes it is an reactant, 2 denotes it is a intermediary,
	# 3 denotes it is a product of the ENTIRE PROTOCOL
	reagent_type = models.IntegerField(default = 1)

	amount = models.DecimalField(max_digits = 50, decimal_places = 25)

	# (L, mL, g, kg, M), might be better if we had a list of these stored
	unit = models.CharField(max_length = 10)

	# link it and other of the same type to the right protocol
	protocol = models.ForeignKey(Protocol)

	reagent = models.ForeignKey(Reagent)

	def __str__(self):
		return str(self.amount) + self.unit + " " + str(self.reagent)

	def get_protocol(self):
		return str(protocol)

	def get_scaling_type(self):
		if self.scaling_type == 1:
			return "Filler"
		elif self.scaling_type == 2:
			return "Constant"
		elif self.scaling_type == 3:
			return "Linear scaling"

	def get_reagent_type(self):
		if self.reagent_type == 1:
			return "Reactant"
		elif self.reagent_type == 2:
			return "Intermediary"
		elif self.reagent_type == 3:
			return "Product"

class ProtocolStep(models.Model):
	# required fields
	action = models.TextField()

	# 2 denotes isConstant, and 3 denotes isLinear for
	# scaling of the time
	scaling_type = models.IntegerField(default = 2)

	# optional fields
	time = models.IntegerField(blank = True, null = True)
	picture = models.FileField(blank = True, null = True)

	step_number = models.IntegerField()
	protocol = models.ForeignKey(Protocol)

	# link the step to the correct reagents
	associated_reagents = models.ManyToManyField(ReagentForProtocol)

	def __str__(self):
		result = "Step " + str(self.step_number)
		if self.time:
			result = result + " for " + str(self.time) + " seconds"
		return result

	def get_protocol(self):
		return str(self.protocol)

	def get_reagents(self):
		return str(self.associated_reagents.all())

class ProtocolRating(models.Model):
	# need validator for only one rating for each person-protocol pairs
	person = models.ForeignKey(ProfileInfo)
	score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
	protocol = models.ForeignKey(Protocol)
