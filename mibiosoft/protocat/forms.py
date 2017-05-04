from django.contrib.auth.models import User
from django import forms
# from django.contrib.auth import authenticate

class NewMessageForm(forms.Form):
	recipient = forms.CharField(required=False)
	message = forms.CharField(widget=forms.Textarea)

	def clean(self, *args, **kwargs):
		# print(self.cleaned_data)
		return super(NewMessageForm, self).clean(*args, **kwargs)