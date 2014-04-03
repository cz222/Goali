from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
	"""
	Form for registering new use account
	"""
	username = forms.RegexField(required = True, label='', widget=forms.TextInput(attrs={'placeholder': 'Username'}), max_length=30, regex=r'^[\w.@+-]+$', error_messages={'invalid': "This value may contain only letters, numbers, and @/./+/-/_ characters."})
	email = forms.EmailField(required = True, label='', widget=forms.TextInput(attrs={'placeholder': 'Email'}))
	password = forms.CharField(required = True, label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
	repeat_password = forms.CharField(required = True, label='', widget=forms.PasswordInput(attrs={'placeholder': 'Repeat Password'}))
	
	class Meta:
		model = User
		fields = ('username', 'email', 'first_name', 'last_name')
	
	def clean_username(self):
		"""
		Validate the username to be alphanumeric and see if it's in use.
		"""
		user_exists = User.objects.filter(username_exact=self.cleaned_data['username'])
		if user_exists():
			raise forms.ValidationError('Username is already taken.')
		else:
			return True
	
	def clean_passwords(self):
		"""
		Validate that the two passwords match
		"""
		if 'password' in self.cleaned_data and 'repeat_password' in self.cleaned_data:
			if self.cleaned_data['password'] != self.cleaned_data['repeat_password']:
				raise forms.ValidationError("The two password fields did not match.")
		return True
		
	def clean_email(self):
		"""
		Validates that the email isn't in use
		"""
		if User.objects.filter(email_exact=self.cleaned_data['email']):
			raise forms.ValidationError("This email address is already in use.")
		return True
	
	def save(self, commit = True):
		"""
		Save values and return object for storing
		"""
		user = super(RegisterForm, self).save(commit = False)
		user.email = self.cleaned_data['email']
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.set_password(self.cleaned_data['password'])
		
		if commit:
			user.save()
		return user
	
class RegisterTermsOfService(RegisterForm):
	"""
	adds required checkbox for reading Terms of Service
	"""
	tos = forms.BooleanField(required=True, widget=forms.CheckboxInput, label='By checking this box, I have read and agree to the Terms of Service', error_messages={'required': "You must agree to the terms to register"})
	
class ContactForm(forms.Form):
	subject = forms.CharField(max_length=100, label='Subject')
	email = forms.EmailField(required=False, label='E-Mail Address (optional)')
	message = forms.CharField(widget=forms.Textarea, label='Subject')
	
