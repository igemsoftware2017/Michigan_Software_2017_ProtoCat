from django.db import models
from django.contrib.auth.models import User
# added
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

'''
This page is to create python classes, which are then converted in to tables for our database
So things like, User, Protocol, Reagents, etc.
'''

# connected to built in user but allow a picture
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

# data containing the name of the category and the category it is contained in
class Category(models.Model):
	title = models.TextField()
	author = models.ForeignKey(User)
	description = models.TextField()
	parent_category = models.ForeignKey('self', blank = True, null = True)

	def __str__(self):
		return self.title

# the generic reagent that has links to the correct associated_reagents
class Reagent(models.Model):
	name = models.TextField()
	picture = models.FileField(blank = True, null = True)
	website = models.URLField(blank = True, null = True)

	def __str__(self):
		return self.name

	def get_website(self):
		return self.website

# has links to all the important parts of the protocol
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

	def __str__(self):
		return self.title

	def get_reagents(self):
		return str(ReagentForProtocol.objects.filter(protocol = self))

	def get_steps(self):
		return str(ProtocolStep.objects.filter(protocol = self))

	def get_total_ratings(self):
		all_ratings = ProtocolRating.objects.filter(protocol = self)
		total = 0
		for rating in all_ratings:
			total = total + rating.score
		return total

	def get_number_ratings(self):
		return ProtocolRating.objects.filter(protocol = self).count()

	def get_average_ratings(self):
		all_ratings = ProtocolRating.objects.filter(protocol = self)
		count = all_ratings.count()
		if (count == 0):
			return "No ratings"
		total = 0
		for rating in all_ratings:
			total = total + rating.score
		count = all_ratings.count()
		return total / count

# just a text field for the reagents if they don't want to be fancy
class TextReagent(models.Model):
	reagents = models.TextField();
	protocol = models.OneToOneField(Protocol)
	def __str__(self):
		return reagents

# the data for each protocol step
class ProtocolStep(models.Model):
	# required fields
	action = models.TextField()

	# 2 denotes isConstant, and 3 denotes isLinear for
	# scaling of the time
	SCALING_TYPES = (
		(1, 'Constant'),
		(2, 'Linear Scaling')
	)
	time_scaling = models.IntegerField(blank = True, null = True,
						default = 2, choices=SCALING_TYPES)

	# optional fields
	time = models.IntegerField(blank = True, null = True)

	step_number = models.IntegerField()
	protocol = models.ForeignKey(Protocol)

	def __str__(self):
		result = "Step " + str(self.step_number)
		if self.time:
			result = result + " for " + str(self.time) + " seconds"
		return result

	def get_protocol(self):
		return str(self.protocol)

# this is the instance of a reagent in a protocol step
class ReagentForProtocol(models.Model):
	# 1 denotes isFiller, 2 denotes isConstant, and 3 denotes isLinear for
	# scaling of the amounts.
	SCALING_TYPES = (
		(1, 'Filling'),
		(2, 'Constant'),
		(3, 'Linear Scaling')
	)
	scaling_type = models.IntegerField(default = 3, choices=SCALING_TYPES)

	# 1 denotes it is an reactant, 2 denotes it is a intermediary,
	# 3 denotes it is a product of the ENTIRE PROTOCOL
	REAGENT_TYPES = (
		(1, 'Reactant'),
		(2, 'Intermediary'),
		(3, 'Product')
	)
	reagent_type = models.IntegerField(default = 1, choices=REAGENT_TYPES)

	amount = models.DecimalField(max_digits = 50, decimal_places = 25)

	# (L, mL, g, kg, M), might be better if we had a list of these stored
	unit = models.CharField(max_length = 10)

	# link it and other of the same type to the right protocol
	protocol = models.ForeignKey(Protocol)

	# link the step to the correct reagents
	protocol_step = models.ForeignKey(ProtocolStep)

	# link it to the correct generic reagent
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

# data relating a user to a protocol with the score
class ProtocolRating(models.Model):
	# need validator for only one rating for each person-protocol pairs
	person = models.ForeignKey(ProfileInfo)
	score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
	protocol = models.ForeignKey(Protocol)

# allow for each user to write their own private notes on each protocol step
class ProtocolStepNotes(models.Model):
	person = models.ForeignKey(ProfileInfo)
	protocol_step = models.ForeignKey(ProtocolStep)
	note = models.TextField()
