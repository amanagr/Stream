from django import forms
from .models import User

class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		user = User.objects.filter(username=username)
		if user.count() == 1:
			if user.first().password == password :
				
				return super(UserLoginForm, self).clean(*args, **kwargs)

			else:
				raise forms.ValidationError("Enter a valid password")
		else :
			raise forms.ValidationError("Invalid User")

		

class UserRegisterForm(forms.Form):
	username = forms.CharField( label = "Username")
	password = forms.CharField(widget=forms.PasswordInput, label = "Password")
	email    = forms.EmailField(label = "Email Address")
	email2   = forms.EmailField(label='Confirm Email')

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		email    = self.cleaned_data.get('email')
		email2   = self.cleaned_data.get('email2')

		if email != email2 :
			raise forms.ValidationError("Emails do not match")

		if User.objects.filter(username=username).exists():
			raise forms.ValidationError("Username already exists")

		return super(UserRegisterForm, self).clean(*args, **kwargs)