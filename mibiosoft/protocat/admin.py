from django.contrib import admin
from .models import Protocol, Protocol_Category, Reagent, Profile_Info

# Register your models here.
admin.site.register(Protocol)
admin.site.register(Profile_Info)
admin.site.register(Reagent)
admin.site.register(Protocol_Category)
