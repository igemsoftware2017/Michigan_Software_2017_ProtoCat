from django.contrib import admin
from .models import *



# Information for a better /admin/ site

class ProfileInfoAdmin(admin.ModelAdmin):
	list_display = ["__str__", "email", "is_admin", "date_joined"]
	class Meta:
		model = ProfileInfo

class CategoryAdmin(admin.ModelAdmin):
	list_display = ["__str__", "parent_category", "author"]
	class Meta:
		model = Category

class ReagentAdmin(admin.ModelAdmin):
	list_display = ["__str__", "get_website"]
	class Meta:
		model = Reagent

class ProtocolAdmin(admin.ModelAdmin):
	list_display = ["__str__", "get_total_ratings", "get_number_ratings", "scaleable", "searchable", "avg_rating", "num_ratings", "category", "get_reagents", "author", "previous_revision", "upload_date", "materials"]
	class Meta:
		model = Protocol

class ReagentForProtocolAdmin(admin.ModelAdmin):
	list_display = ["__str__", "get_scaling_type", "get_reagent_type"]
	class Meta:
		model = ReagentForProtocol

class ProtocolStepAdmin(admin.ModelAdmin):
	list_display = ["__str__", "protocol", "action"]
	class Meta:
		model = ProtocolStep

class ProtocolRatingAdmin(admin.ModelAdmin):
	list_display = ["person", "score", "protocol"]
	class Meta:
		model = ProtocolRating

class ProtocolCommentAdmin(admin.ModelAdmin):
	class Meta:
		model = ProtocolComment

class GithubIdAdmin(admin.ModelAdmin):
	class Meta:
		model = GithubId


class Favourite_ProtocolAdmin(admin.ModelAdmin):
	list_display = ["__str__", "fav_protocol"]
	class Meta:
		model = Favourite_Protocol

class OrganizationAdmin(admin.ModelAdmin):
	list_display = ["__str__", "get_members"]

class MembershipAdmin(admin.ModelAdmin):
	list_display = ["organization", "user"]
class MessageAdmin(admin.ModelAdmin):
	class Meta:
		model = Message

class Organization_ProtocolAdmin(admin.ModelAdmin):
	list_display = ["__str__", "protocol"]
# Register your models here.

admin.site.register(ProfileInfo, ProfileInfoAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Reagent, ReagentAdmin)
admin.site.register(Protocol, ProtocolAdmin)
admin.site.register(ProtocolStep, ProtocolStepAdmin)
admin.site.register(ReagentForProtocol, ReagentForProtocolAdmin)
admin.site.register(ProtocolRating, ProtocolRatingAdmin)
admin.site.register(ProtocolComment, ProtocolCommentAdmin)
admin.site.register(GithubId, GithubIdAdmin)
admin.site.register(Favourite_Protocol, Favourite_ProtocolAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(Organization_Protocol, Organization_ProtocolAdmin)
admin.site.register(Message, MessageAdmin)
