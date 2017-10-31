from django.db import models
from django.contrib.auth.models import User
# added
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

'''
This page is to create python classes, which are then converted in to tables for our database
So things like, User, Protocol, Reagents, etc.
'''

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# connected to built in user but allow a picture
class ProfileInfo(models.Model):
	user = models.OneToOneField(User, related_name='profileinfo', on_delete = models.CASCADE)
	profile_image = models.ImageField(blank = True, null = True, upload_to = "media")
	about = models.TextField(blank = True, null = True)
	contact_info = models.TextField(blank = True, null = True)
	meows = models.IntegerField(default = 0)
	favorites = models.ManyToManyField('Protocol', blank = True)

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
	author = models.ForeignKey(ProfileInfo)
	description = models.TextField()
	upload_date = models.DateTimeField(auto_now_add = True)
	parent_category = models.ForeignKey('self', blank = True, null = True)

	def __str__(self):
		return self.title

# the generic reagent that has links to the correct associated_reagents
class Reagent(models.Model):
	name = models.TextField()
	description = models.TextField(blank = True, null = True, default = "")
	website = models.URLField(blank = True, null = True)

	def __str__(self):
		return self.name

	def get_website(self):
		return self.website



# has links to all the important parts of the protocol
class Protocol(models.Model):
	title = models.TextField()
	author = models.ForeignKey(ProfileInfo, related_name="protocols")
	description = models.TextField(blank = True, null = True)
	materials = models.TextField(default = "", blank = True, null = True)

	# Allow the revisionist to describe changes made
	change_log = models.TextField(blank = True, null = True)

	# many protocols to one category
	category = models.ForeignKey(Category, blank = True, null = True, related_name="protocol_for_category")

	# True if the author want dynamic scaling of products and reactants
	scaleable = models.BooleanField(default = False)
	searchable = models.BooleanField(default = True)

	upload_date = models.DateTimeField(auto_now_add = True)

	num_ratings = models.IntegerField(default = 0)

	avg_rating = models.DecimalField(default = 0, max_digits = 50, decimal_places = 25)

	num_steps = models.IntegerField(default = 0)

	# many branching protocols to one parent protocol
	previous_revision = models.ForeignKey('self', related_name='previous_revision1', blank = True, null = True)
	first_revision = models.ForeignKey('self', related_name='first_revision1', blank = True, null = True)

	def __str__(self):
		return self.title

	def type(self):
		return "Protocol"

	def get_previous_revision(self):
		return previous_revision

	def get_first_revisions(self):
		return first_revision

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
			return "N/A"
		total = 0
		for rating in all_ratings:
			total = total + rating.score
		count = all_ratings.count()
		return float(total) / count


# favourite protocol
class Favourite_Protocol(models.Model):
	user = models.ForeignKey(ProfileInfo)
	fav_protocol = models.ForeignKey(Protocol)
	#add note for Favourite_Protocol
	def __str__(self):
		return str(self.user)
	def get_user_protocol(self):
		return self.fav_protocol
	def get_protocol_by_user(self):
		return self.objects.filter(user = self.user)
	def get_user_by_protocol(self):
		return self.objects.filter(fav_protocol = self.fav_protocol)

#Add Group
#Each User can be in multiple groups
class Organization(models.Model):
    #TODO:orginaziation many to many field
    name = models.TextField()
    description = models.TextField()
    organization_image = models.ImageField(blank = True, null = True, upload_to = "media")
    def __str__(self):
        return str(self.name)
    def get_members(self):
        users = Membership.objects.filter(organization = self)
        resultArray = []
        for x in users:
            resultArray.append(str(x.user))
        return resultArray

class Membership(models.Model):
    organization = models.ForeignKey(Organization)
    user = models.ForeignKey(ProfileInfo)
    isAdmin = models.BooleanField()
    def __str__(self):
        return str(self.user)

class Organization_Protocol(models.Model):
    organization = models.ForeignKey(Organization)
    protocol = models.ForeignKey(Protocol)
    def __str__(self):
        return str(self.organization)


# the data for each protocol step
class ProtocolStep(models.Model):
	title = models.TextField(default = "")
	action = models.TextField()

	# 2 denotes isConstant, and 3 denotes isLinear for
	# scaling of the time
	SCALING_TYPES = (
		(0, 'N/A'),
		(1, 'Constant'),
		(2, 'Linear Scaling')
	)
	time_scaling = models.IntegerField(default = 2, choices=SCALING_TYPES)

	# optional fields
	time = models.IntegerField(default = -1)

	step_number = models.IntegerField()
	protocol = models.ForeignKey(Protocol, related_name="protocol_step")
	warning = models.TextField(default = "")

	def __str__(self):
		result = "Step " + str(self.step_number)
		if self.time:
			result = result + " for " + str(self.time) + " seconds"
		return result

	def get_protocol(self):
		return str(self.protocol)

	def get_understandable_scaling_type(self):
		if (self.time_scaling == 1):
			return "Constant"
		elif (self.time_scaling == 2):
			return "Linear Scaling"
		else:
			return None

# this is the instance of a reagent in a protocol step
class ReagentForProtocol(models.Model):
	# 1 denotes isFiller, 2 denotes isConstant, and 3 denotes isLinear for
	# scaling of the amounts.
	SCALING_TYPES = (
		(1, 'Filling'),
		(2, 'Constant'),
		(3, 'Linear Scaling')
	)
	scaling_type = models.IntegerField(default = 2, choices=SCALING_TYPES)

	# 1 denotes it is an reactant, 2 denotes it is a intermediary,
	# 3 denotes it is a product of the ENTIRE PROTOCOL
	REAGENT_TYPES = (
		(1, 'Reactant'),
		(2, 'Intermediary'),
		(3, 'Product'),
		(4, 'Catalyst')
	)
	reagent_type = models.IntegerField(default = 1, choices=REAGENT_TYPES)

	amount = models.DecimalField(max_digits = 50, decimal_places = 25)

	UNIT_TYPES = (
		('L', 'Liters'),
		('g', 'Grams')
	)

	unit = models.CharField(max_length = 25, choices = UNIT_TYPES)

	# link it and other of the same type to the right protocol
	protocol = models.ForeignKey(Protocol)

	# link the step to the correct reagents
	protocol_step = models.ForeignKey(ProtocolStep, related_name = "reagents_for_step")
	protocol_step_number = models.IntegerField();

	number_in_step = models.IntegerField()

	significant_figures = models.IntegerField();
	display_name = models.TextField(blank = True, null = True)
	preserve_units = models.IntegerField(blank = True, null = True)

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
	protocol = models.ForeignKey(Protocol, related_name="ratings_for_protocol")

# allow for each user to write their own private notes on each protocol step
class ProtocolComment(models.Model):
	author = models.ForeignKey(ProfileInfo)
	protocol = models.ForeignKey(Protocol, related_name="comments_for_protocol")
	upload_date = models.DateTimeField(auto_now_add = True)
	note = models.TextField()

	def __str__(self):
		return self.note

	def type(self):
		return "Note"

class GithubId(models.Model):
	name = models.TextField()
	def __str__(self):
		return self.name

class Message(models.Model):
	sender = models.ForeignKey(ProfileInfo, related_name="sender_user")
	recipient = models.ForeignKey(ProfileInfo, related_name="recip_user")
	message = models.TextField()
	timeSent = models.DateTimeField(null = True, auto_now_add = True)
	deleted = models.BooleanField(default = False)
	read = models.BooleanField(default = False)

	def __str__(self):
		return self.sender.username + " to " + self.recipient.username

class MetricQuestion(models.Model):
	QUESTION_TYPES = (
		('N', 'Number'),
		('T', 'Text')
	)

	protocol = models.ForeignKey(Protocol, related_name="metric_questions")
	question_text = models.TextField()
	question_type = models.CharField(max_length = 1, choices = QUESTION_TYPES)

class MetricResponse(models.Model):
	question = models.ForeignKey(MetricQuestion, related_name="responses")
	timestamp = models.DateTimeField(null = True, auto_now_add = True)
	response = models.TextField()
	user = models.ForeignKey(ProfileInfo)

class MetricEnumQuestion(models.Model):
	protocol = models.ForeignKey(Protocol, related_name="metric_enum_questions")
	question_text = models.TextField()

class MetricEnumOption(models.Model):
	enum_question = models.ForeignKey(MetricEnumQuestion, related_name="options")
	option_text = models.TextField()

class MetricEnumResponse(models.Model):
	question = models.ForeignKey(MetricEnumQuestion, related_name="responses")	
	response = models.ForeignKey(MetricEnumOption)
	timestamp = models.DateTimeField(null = True, auto_now_add = True)
	user = models.ForeignKey(ProfileInfo)

