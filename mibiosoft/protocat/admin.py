from django.contrib import admin
from .models import ProfileInfo, Reagent, Category, Protocol, ProtocolStep, ReagentForProtocol



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
	list_display = ["__str__"]
	class Meta:
		model = Reagent

class ProtocolAdmin(admin.ModelAdmin):
	list_display = ["__str__", "category", "author", "last_revision", "upload_date"]
	class Meta:
		model = Protocol

class ProtocolStepAdmin(admin.ModelAdmin):
	list_display = ["__str__"]
	class Meta:
		model = ProtocolStep

class ReagentForProtocolAdmin(admin.ModelAdmin):
	list_display = ["__str__"]
	class Meta:
		model = ReagentForProtocol

# Register your models here.

admin.site.register(ProfileInfo, ProfileInfoAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Reagent, ReagentAdmin)
admin.site.register(Protocol, ProtocolAdmin)
admin.site.register(ProtocolStep, ProtocolStepAdmin)
admin.site.register(ReagentForProtocol, ReagentForProtocolAdmin)
