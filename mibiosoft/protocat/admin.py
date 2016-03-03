from django.contrib import admin
from .models import Protocol, Category, Reagent, ProfileInfo



# Information for a better /admin/ site

class ProtocolAdmin(admin.ModelAdmin):
	list_display = ["__str__", "category", "author", "last_revision", "upload_date"]
	class Meta:
		model = Protocol

class ProfileInfoAdmin(admin.ModelAdmin):
	list_display = ["__str__", "email", "is_admin", "date_joined"]
	class Meta:
		model = ProfileInfo

class ReagentAdmin(admin.ModelAdmin):
	list_display = ["__str__"]
	class Meta:
		model = Reagent

class CategoryAdmin(admin.ModelAdmin):
	list_display = ["__str__", "parent_category", "author"]
	class Meta:
		model = Category

# Register your models here.

admin.site.register(Protocol, ProtocolAdmin)
admin.site.register(ProfileInfo, ProfileInfoAdmin)
admin.site.register(Reagent, ReagentAdmin)
admin.site.register(Category, CategoryAdmin)
