from django.contrib import admin
from .models import ProfileInfo, Reagent, Category, Protocol, ProtocolStep, ReagentForProtocol, Rating



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
	list_display = ["__str__", "is_scaleable", "is_searchable", "get_category", "get_reagents", "author", "last_revision", "upload_date"]
	class Meta:
		model = Protocol

class ReagentForProtocolAdmin(admin.ModelAdmin):
	list_display = ["__str__", "get_scaling_type", "get_reagent_type"]
	class Meta:
		model = ReagentForProtocol

class ProtocolStepAdmin(admin.ModelAdmin):
	list_display = ["__str__", "get_protocol", "get_reagents", "action"]
	class Meta:
		model = ProtocolStep

class RatingAdmin(admin.ModelAdmin):
	list_display = ["person", "score", "protocol"]
	class Meta:
		model = Rating

# Register your models here.

admin.site.register(ProfileInfo, ProfileInfoAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Reagent, ReagentAdmin)
admin.site.register(Protocol, ProtocolAdmin)
admin.site.register(ProtocolStep, ProtocolStepAdmin)
admin.site.register(ReagentForProtocol, ReagentForProtocolAdmin)
admin.site.register(Rating, RatingAdmin)
