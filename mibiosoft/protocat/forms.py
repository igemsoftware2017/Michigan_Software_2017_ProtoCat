from django import forms

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='Email address', max_length=100) 

class NewPasswordForm(forms.Form):
    new_password1 = forms.CharField(widget=forms.PasswordInput(), max_length=100)
    new_password2 = forms.CharField(widget=forms.PasswordInput(), max_length=100)

