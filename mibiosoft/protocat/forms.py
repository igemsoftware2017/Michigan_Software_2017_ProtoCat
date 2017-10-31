from django.contrib.auth.models import User
from django import forms
import bleach
# from django.contrib.auth import authenticate

class NewMessageForm(forms.Form):
	recipient = forms.CharField(required=False, label="To")
	message = forms.CharField(widget=forms.Textarea, required=False)

	def clean(self, *args, **kwargs):
		recip = self.cleaned_data.get('recipient')
		print('here')
		try:
			 User.objects.get(username=recip)
		except:
			raise forms.ValidationError("User does not exist")

		if self.cleaned_data.get('message').strip() == "":
			raise forms.ValidationError("Message cannot be empty")

		cleaned_data = super(NewMessageForm, self).clean(*args, **kwargs)
		cleaned_data['message'] = bleach.clean(self.data['message'])
		return cleaned_data